import os
import streamlit as st
from pypdf import PdfReader
from io import BytesIO
from langchain_aws import ChatBedrock
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Configuration
BEDROCK_MODEL = "anthropic.claude-3-sonnet-20240229-v1:0"
AWS_REGION = "us-east-1"
TEMPERATURE = 0.7

# Initialize LLM
@st.cache_resource(show_spinner=False)
def init_llm():
    return ChatBedrock(
        model_id=BEDROCK_MODEL,
        model_kwargs={"temperature": TEMPERATURE},
        region_name=AWS_REGION
    )

# Create Chain
def create_qa_chain(llm):
    prompt_template = """Here's an article:

<article>
{article}
</article>

{question}"""
    
    PROMPT = PromptTemplate(
        template=prompt_template, 
        input_variables=["article", "question"]
    )
    
    chain = LLMChain(
        llm=llm,
        prompt=PROMPT,
        verbose=True  # Enable chain logging
    )
    
    return chain

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.llm = init_llm()
    st.session_state.chain = create_qa_chain(st.session_state.llm)

# Streamlit UI
st.title("📝 File Q&A with Claude 3.5 Sonnet")

# File upload
uploaded_file = st.file_uploader(
    "Upload an article", 
    type=("txt", "md", "pdf")
)

question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:
    try:
        # Read file content based on file type
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(BytesIO(uploaded_file.read()))
            article = "\n".join(page.extract_text() for page in pdf_reader.pages)
        else:
            article = uploaded_file.read().decode()
        
        # Show file content in expander
        with st.expander("View article content"):
            st.text(article)
        
        # Get answer using LangChain
        result = st.session_state.chain.invoke({
            "article": article,
            "question": question
        })
        
        # Show answer
        st.write("### Answer")
        st.write(result["text"])
            
    except Exception as e:
        st.error(f"Error: {str(e)}")