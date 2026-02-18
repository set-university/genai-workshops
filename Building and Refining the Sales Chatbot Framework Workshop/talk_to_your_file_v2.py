import os
import warnings
import logging
import sys

# Configure logging and warnings before any imports
logging.getLogger().setLevel(logging.ERROR)
warnings.filterwarnings('ignore')
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
os.environ["TORCH_SHOW_CPP_STACKTRACES"] = "0"

# Now import everything else
import streamlit as st
import boto3
import json
from pypdf import PdfReader
from io import BytesIO
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_aws import ChatBedrock
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Configuration
PERSIST_DIR = "db"  # ChromaDB persistence directory
CHUNK_SIZE = 1000   # Size of text chunks
CHUNK_OVERLAP = 200  # Overlap between chunks
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Model for embeddings
NUM_CHUNKS = 10  # Number of relevant chunks to retrieve
BEDROCK_MODEL = "anthropic.claude-sonnet-4-20250514-v1:0"
AWS_REGION = "us-east-1"
TEMPERATURE = 0.1

# Initialize embeddings and vectorstore
@st.cache_resource(show_spinner=False)
def init_vectorstore():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    os.makedirs(PERSIST_DIR, exist_ok=True)
    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="documents"
    )
    
    return vectorstore

# Initialize LLM
@st.cache_resource(show_spinner=False)
def init_llm():
    return ChatBedrock(
        model_id=BEDROCK_MODEL,
        model_kwargs={"temperature": TEMPERATURE},
        region_name=AWS_REGION
    )

# Create QA Chain
def create_qa_chain(vectorstore, llm):
    prompt_template = """Use the following pieces of context to answer the question. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context: {context}
    
    Question: {question}

    If you doesn't have answer from the cotext, write "I can not answer based on the context".
    
    Answer:"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, 
        input_variables=["context", "question"]
    )
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": NUM_CHUNKS}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
        verbose=True
    )
    
    return chain

# Initialize session state for non-widget values only
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.vectorstore = None
    st.session_state.llm = None
    st.session_state.qa_chain = None
    st.session_state.processed_files = set()

# Initialize components if not already done
if st.session_state.vectorstore is None:
    st.session_state.vectorstore = init_vectorstore()
    st.session_state.llm = init_llm()
    st.session_state.qa_chain = create_qa_chain(
        st.session_state.vectorstore,
        st.session_state.llm
    )

# Streamlit UI
st.title("📚 Document Q&A")

# File upload without session state
uploaded_files = st.file_uploader(
    "Upload documents", 
    type=["txt", "md", "pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.processed_files:
            with st.spinner(f"Processing {file.name}..."):
                try:
                    # Process file content
                    if file.type == "application/pdf":
                        pdf_reader = PdfReader(BytesIO(file.read()))
                        content = "\n".join(page.extract_text() for page in pdf_reader.pages)
                    else:
                        content = file.read().decode()
                    
                    # Split text
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=CHUNK_SIZE,
                        chunk_overlap=CHUNK_OVERLAP,
                        separators=["\n\n", "\n", " ", ""]
                    )
                    chunks = text_splitter.split_text(content)
                    
                    # Add to vectorstore
                    st.session_state.vectorstore.add_texts(
                        texts=chunks,
                        metadatas=[{"filename": file.name, "type": file.type}] * len(chunks)
                    )
                    
                    st.session_state.processed_files.add(file.name)
                    st.success(f"Processed {file.name}")
                except Exception as e:
                    st.error(f"Error processing {file.name}: {str(e)}")

# Question answering using chat input
if question := st.chat_input("Ask a question about your documents"):
    try:
        # Get answer
        result = st.session_state.qa_chain.invoke({"query": question})
        answer = result["result"]
        source_docs = result["source_documents"]
        
        # Show answer and sources
        st.write("### Answer")
        st.write(answer)
        
        with st.expander("View sources"):
            for doc in source_docs:
                st.markdown(f"""
                **From**: {doc.metadata.get('filename', 'Unknown')}
                **Text**: \n\n{doc.page_content}
                ---
                """)
                
    except Exception as e:
        st.error(f"Error: {str(e)}") 