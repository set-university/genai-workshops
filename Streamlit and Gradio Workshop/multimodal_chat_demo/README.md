# Multi-modal AI Chat (Gradio)

A chatbot that accepts text, images, and files — powered by GPT-4o with streaming responses.

## What it does

- Send text messages and get AI responses in real time (streamed token by token)
- Upload images and ask questions about them (GPT-4o Vision)
- Upload text files for analysis
- Full conversation history with multi-turn context

## Why Gradio?

Gradio is the natural choice for this demo because:

- **`gr.ChatInterface`** gives you a production-ready chat UI in ~10 lines of code — with multimodal input, streaming, examples, and history built in
- **Multimodal input** is a first-class feature: set `multimodal=True` and users can drag-and-drop images/files alongside text
- **Streaming** works out of the box — just `yield` partial responses from your function
- **ML/AI-first design** — Gradio was built specifically for wrapping ML models in web interfaces, so the chat + media workflow feels native rather than bolted on

Streamlit has `st.chat_input` / `st.chat_message`, but building multimodal chat with file uploads and streaming requires significantly more boilerplate. Gradio handles this in a single component.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key-here
python app.py
```
