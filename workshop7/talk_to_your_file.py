import streamlit as st
import boto3
import json
from pypdf import PdfReader
from io import BytesIO

st.title("📝 File Q&A with Claude 3.5 Sonnet")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"))
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

def read_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

if uploaded_file and question:
    # Read file content based on file type
    if uploaded_file.type == "application/pdf":
        article = read_pdf(BytesIO(uploaded_file.read()))
    else:
        article = uploaded_file.read().decode()
    
    # Show file content in expander
    with st.expander("View article content"):
        st.text(article)
    
    # Initialize Bedrock client using default AWS configuration
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-east-1'  # Change this if using a different region
    )
    
    # Prepare the prompt
    prompt = f"""Here's an article:

<article>
{article}
</article>

{question}"""

    # Prepare the request body
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    })

    try:
        # Invoke the model
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=body
        )
        
        # Parse the response
        response_body = json.loads(response.get('body').read())
        answer = response_body['content'][0]['text']
        
        st.write("### Answer")
        st.write(answer)
        
    except Exception as e:
        st.error(f"Error: {str(e)}")