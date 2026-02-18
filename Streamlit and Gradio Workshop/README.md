# Gradio & Streamlit Workshop

Three demos showcasing when and why to use **Gradio** vs **Streamlit** for AI-powered applications.

## Demos

| Demo | Framework | Description |
|------|-----------|-------------|
| [**Multi-modal AI Chat**](multimodal_chat_demo/) | Gradio | Chat with GPT-4o — send text, images, files. Streaming responses. |
| [**Voice Assistant**](voice_assistant_demo/) | Gradio | Speak into the mic → Whisper transcribes → GPT-4o responds → TTS speaks back. |
| [**AI Analytics Dashboard**](analytics_dashboard_demo/) | Streamlit | Multi-page app: dashboard + chat with your data + interactive data editor. |

## When to use what?

**Gradio** — best for wrapping AI/ML models in a web UI:
- Multimodal inputs (images, audio, video, files) as first-class components
- Real-time streaming and media processing
- Quick prototyping: production-ready chat UI in ~10 lines
- Ideal for: chatbots, voice apps, image/video processing, model demos

**Streamlit** — best for data applications and dashboards:
- Native multi-page apps with shared state
- Interactive data editing (`st.data_editor`)
- Rich layout: sidebar filters, columns, metrics, charts
- Ideal for: dashboards, analytics tools, data exploration, internal tools

## Setup

```bash
conda create -n genai_workshop python=3.10
conda activate genai_workshop
pip install -r requirements.txt
```

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your-key-here
```

## Run

```bash
# Demo 1: Multi-modal AI Chat
cd multimodal_chat_demo && python app.py

# Demo 2: Voice Assistant
cd voice_assistant_demo && python app.py

# Demo 3: AI Analytics Dashboard
cd analytics_dashboard_demo && streamlit run app.py
```

## Deployment

Gradio apps are easy to share and deploy beyond your local machine:

### Quick sharing

Run with `share=True` — Gradio generates a public `*.gradio.live` URL (valid for 72 hours). Perfect for quick demos, client reviews, or sharing with another team.

### Hugging Face Spaces

Deploy your Gradio app directly to [Hugging Face Spaces](https://huggingface.co/spaces) — free hosting with GPU support. Just push your code to a HF repo and it runs automatically.

### Docker

Containerize any demo to ship to a client, hand off to another team, or deploy to any cloud. Example for `multimodal_chat_demo`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python", "app.py"]
```

```bash
# Build and run
cd multimodal_chat_demo
docker build -t multimodal-chat .
docker run -p 7860:7860 -e OPENAI_API_KEY=your-key-here multimodal-chat
```

The same approach works for any demo — just change the port and entry command (`streamlit run app.py` for Streamlit).
