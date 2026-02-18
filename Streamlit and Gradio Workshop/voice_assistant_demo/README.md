# Voice Assistant (Gradio)

A real-time voice assistant — speak into your microphone, get a streaming text response and hear it spoken back.

## What it does

- **Speech-to-Text**: Record from microphone → Whisper API transcribes your speech
- **AI Response**: GPT-4o generates a concise answer (streamed token by token)
- **Text-to-Speech**: The response is spoken aloud using OpenAI TTS (Nova voice)
- Full conversation history maintained across turns
- Also supports text input for accessibility

## Why Gradio?

Gradio is the only practical choice here because:

- **Native media components** — `gr.Audio(sources=["microphone"])` gives you browser-based mic recording with zero frontend code
- **Event chaining** — `.stop_recording().then()` lets you build a pipeline: record → transcribe → respond → speak, all declared in Python
- **Real-time streaming** — streaming text responses while audio plays back is straightforward with generators
- **Hardware access** — Gradio's components handle browser permissions for microphone access seamlessly

Streamlit has no native microphone input component. You'd need a third-party widget (like `streamlit-webrtc`), custom JavaScript, and significant workarounds for streaming. Gradio makes this a ~100-line app.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key-here
python app.py
```
