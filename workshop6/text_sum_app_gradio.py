import gradio as gr
from transformers import pipeline

# Load summarization model from Hugging Face
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Gradio app for text summarization
def gradio_summarization_app(input_text):
    # Generate summary
    summary = summarizer(input_text, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
    return summary

# Create Gradio interface
gradio_interface = gr.Interface(
    fn=gradio_summarization_app,
    inputs="text",
    outputs="text",
    title="Text Summarization App",
    description="Enter text to summarize and get a concise summary"
)

# Launch the Gradio app
if __name__ == "__main__":
    gradio_interface.launch(share=True)