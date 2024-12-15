import streamlit as st
from transformers import pipeline

# Load summarization model from Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Streamlit app for text summarization
def streamlit_summarization_app():
    st.title("Text Summarization App")
    
    # Input text
    input_text = st.text_area("Enter text to summarize", height=300)
    
    # Button to trigger summarization
    if st.button("Summarize"):
        if input_text:
            # Generate summary
            summary = summarizer(input_text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter some text to summarize")

# Run the Streamlit app
if __name__ == "__main__":
    streamlit_summarization_app()