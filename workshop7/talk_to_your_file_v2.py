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

# Configuration
PERSIST_DIR = "db"  # ChromaDB persistence directory
CHUNK_SIZE = 1000   # Size of text chunks
CHUNK_OVERLAP = 200  # Overlap between chunks
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Model for embeddings
NUM_CHUNKS = 3  # Number of relevant chunks to retrieve
BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"  # Claude model version
AWS_REGION = "us-east-1"  # AWS region for Bedrock
TEMPERATURE = 0.7  # Temperature for response generation

# Suppress warnings
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', message='.*Tried to instantiate.*')

# Initialize ChromaDB with persistence
os.makedirs(PERSIST_DIR, exist_ok=True)

@st.cache_resource(show_spinner=False)
def init_chromadb():
    """Initialize ChromaDB with persistence and transformer embeddings"""
    # Set environment variable to suppress torch warnings
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL,
        normalize_embeddings=True
    )
    
    # Get or create collection
    try:
        collection = client.get_collection(
            name="documents",
            embedding_function=embedding_function
        )
    except:
        collection = client.create_collection(
            name="documents",
            embedding_function=embedding_function
        )
    
    return client, collection

# Initialize database once
if 'collection' not in st.session_state:
    client, collection = init_chromadb()
    st.session_state.client = client
    st.session_state.collection = collection

# Use the initialized collection
collection = st.session_state.collection

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", " ", ""]
)

def read_pdf(file):
    """Extract text from PDF file"""
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def read_file(uploaded_file):
    """Read content from uploaded file"""
    if uploaded_file.type == "application/pdf":
        return read_pdf(BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode()

def store_document(content, metadata):
    """Store document chunks in ChromaDB"""
    # Split text into chunks
    chunks = text_splitter.split_text(content)
    
    # Add chunks to collection
    collection.add(
        documents=chunks,
        metadatas=[metadata] * len(chunks),
        ids=[f"{metadata['filename']}_{i}" for i in range(len(chunks))]
    )
    return len(chunks)

def get_context(question, k=NUM_CHUNKS):
    """Get relevant context for the question"""
    results = collection.query(
        query_texts=[question],
        n_results=k,
        include=["documents", "metadatas", "distances", "embeddings"]
    )
    return results['documents'][0], results['metadatas'][0], results['distances'][0]

# Streamlit UI
st.title("📚 Document Q&A with Claude 3.5")

# File upload and processing section
uploaded_files = st.file_uploader(
    "Upload documents", 
    type=["txt", "md", "pdf"],
    accept_multiple_files=True,
    key="file_uploader"  # Add key to maintain state
)

# Process uploaded files - only when new files are uploaded
if uploaded_files:
    # Use session state to track processed files
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = set()
    
    # Process only new files
    for file in uploaded_files:
        if file.name not in st.session_state.processed_files:
            with st.spinner(f"Processing {file.name}..."):
                content = read_file(file)
                metadata = {"filename": file.name, "type": file.type}
                num_chunks = store_document(content, metadata)
                st.success(f"Stored {file.name} in {num_chunks} chunks")
                st.session_state.processed_files.add(file.name)

# Question answering section
question = st.text_input("Ask a question about your documents")

if question:
    # Get relevant context with metadata
    chunks, metadatas, distances = get_context(question)
    
    # Prepare prompt for Claude
    prompt = f"""Here are the relevant sections from the documents:

<context>
{' '.join(chunks)}
</context>

Question: {question}

Please answer based on the context provided."""

    # Get answer from Claude
    try:
        bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        response = bedrock.invoke_model(
            modelId=BEDROCK_MODEL,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": TEMPERATURE
            })
        )
        
        answer = json.loads(response.get('body').read())['content'][0]['text']
        
        # Show context details and answer
        with st.expander("View source context", expanded=True):
            st.write("### Source Chunks")
            # Sort chunks by relevance (lowest distance = highest relevance)
            sorted_results = sorted(zip(chunks, metadatas, distances), key=lambda x: x[2])
            
            for chunk, metadata, _ in sorted_results:
                st.markdown(f"""
                **From**: {metadata['filename']}
                **Text**: \n\n{chunk}
                ---
                """)
        st.write("### Answer")
        st.write(answer)
        
    except Exception as e:
        st.error(f"Error getting answer: {str(e)}") 