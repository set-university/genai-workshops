import streamlit as st
import boto3
import json
from pypdf import PdfReader
from io import BytesIO
import chromadb
import os
import warnings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import BedrockChat
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Configuration
PERSIST_DIR = "db"  # ChromaDB persistence directory
CHUNK_SIZE = 1000   # Size of text chunks
CHUNK_OVERLAP = 200  # Overlap between chunks
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Model for embeddings
NUM_CHUNKS = 3  # Number of relevant chunks to retrieve
BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"  # Claude model version
AWS_REGION = "us-east-1"  # AWS region for Bedrock
TEMPERATURE = 0.7  # Temperature for response generation
MAX_HISTORY = 5  # Maximum number of conversation turns to remember

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*Tried to instantiate.*')

# Initialize ChromaDB with persistence
os.makedirs(PERSIST_DIR, exist_ok=True)

# Initialize LangChain chat model
@st.cache_resource(show_spinner=False)
def init_chat_model():
    return BedrockChat(
        model_id=BEDROCK_MODEL,
        model_kwargs={"temperature": TEMPERATURE},
        region_name=AWS_REGION
    )

# Initialize embeddings
@st.cache_resource(show_spinner=False)
def init_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

# Initialize ChromaDB and create retriever
@st.cache_resource(show_spinner=False)
def init_chromadb():
    """Initialize ChromaDB with persistence and transformer embeddings"""
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    # Initialize embeddings
    embeddings = init_embeddings()
    
    # Create or load Chroma vector store
    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="documents"
    )
    
    return vectorstore

# Initialize conversation memory
@st.cache_resource(show_spinner=False)
def init_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

# Create the conversation chain
def create_conversation_chain(llm, retriever, memory):
    template = """You are a helpful and friendly AI assistant who can:
    1. Answer questions about documents that users upload
    2. Remember personal details shared in conversation
    3. Engage in general conversation
    4. Maintain context from previous messages

    Always be polite and personable. If you remember any personal details about the user,
    use them naturally in conversation when appropriate.

    Current conversation:
    {chat_history}

    Context from documents:
    {context}

    Human: {question}
    Assistant:"""

    PROMPT = ChatPromptTemplate.from_template(template)

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": PROMPT},
        return_source_documents=True,
        verbose=True
    )

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'vectorstore' not in st.session_state:
    vectorstore = init_chromadb()
    st.session_state.vectorstore = vectorstore
    st.session_state.llm = init_chat_model()
    st.session_state.memory = init_memory()
    st.session_state.chain = create_conversation_chain(
        st.session_state.llm,
        vectorstore.as_retriever(search_kwargs={"k": NUM_CHUNKS}),
        st.session_state.memory
    )

if 'processed_files' not in st.session_state:
    st.session_state.processed_files = set()

# Streamlit UI
st.title("🤖 AI Assistant & Document Chat")
st.markdown("""
This AI assistant can:
- Answer questions about your uploaded documents
- Remember details from your conversation
- Help with general questions
- Maintain context across the chat
""")

# Sidebar for file upload
with st.sidebar:
    st.header("📄 Document Upload")
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["txt", "md", "pdf"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.processed_files:
                with st.spinner(f"Processing {file.name}..."):
                    # Read file
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
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.session_state.memory.clear()
        st.rerun()

# Chat interface
chat_container = st.container()
with chat_container:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message("assistant" if message["is_assistant"] else "user"):
            st.write(message["content"])
            if message.get("sources"):
                with st.expander("View sources"):
                    for source in message["sources"]:
                        st.markdown(f"""
                        **From**: {source['filename']}
                        **Text**: \n\n{source['text']}
                        ---
                        """)

# User input
if question := st.chat_input("Ask a question about your documents or chat with me"):
    # Add user message to chat
    st.session_state.chat_history.append({"is_assistant": False, "content": question})
    
    # Get response from chain
    try:
        result = st.session_state.chain({"question": question})
        answer = result["answer"]
        sources = []
        
        if result.get("source_documents"):
            for doc in result["source_documents"]:
                sources.append({
                    "filename": doc.metadata.get("filename", "Unknown"),
                    "text": doc.page_content
                })
        
        # Add assistant response to chat
        st.session_state.chat_history.append({
            "is_assistant": True,
            "content": answer,
            "sources": sources if sources else None
        })
        
        # Rerun to update chat display
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}") 