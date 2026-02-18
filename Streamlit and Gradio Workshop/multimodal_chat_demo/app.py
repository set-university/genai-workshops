import base64
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """You are a helpful AI assistant. You can:
- Answer questions about images the user uploads
- Analyze documents and files
- Have general conversations
- Help with coding, writing, and analysis tasks

Be concise but thorough. When analyzing images, describe what you see in detail."""


def build_message_content(message):
    """Convert a Gradio multimodal message into OpenAI API content blocks."""
    content = []

    if message.get("text"):
        content.append({"type": "text", "text": message["text"]})

    for file_path in message.get("files", []):
        if any(file_path.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]):
            with open(file_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            ext = file_path.rsplit(".", 1)[-1].lower()
            mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
                    "gif": "image/gif", "webp": "image/webp"}[ext]
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{b64}"}
            })
        else:
            try:
                with open(file_path, "r") as f:
                    text = f.read()
                content.append({"type": "text", "text": f"File '{file_path.split('/')[-1]}':\n```\n{text}\n```"})
            except Exception:
                content.append({"type": "text", "text": f"[Could not read file: {file_path.split('/')[-1]}]"})

    return content if content else [{"type": "text", "text": ""}]


def chat(message, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for entry in history:
        role = entry.get("role")
        raw = entry.get("content", "")
        if role == "assistant":
            messages.append({"role": "assistant", "content": raw})
        elif role == "user":
            messages.append({"role": "user", "content": raw if isinstance(raw, str) else str(raw)})

    messages.append({"role": "user", "content": build_message_content(message)})

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
        max_tokens=4096,
    )

    response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            response += delta
            yield response


demo = gr.ChatInterface(
    fn=chat,
    multimodal=True,
    title="Multi-modal AI Chat",
    description="Send text, images, or files — powered by GPT-4o with streaming responses.",
    examples=[
        {"text": "What can you help me with?"},
        {"text": "Explain the difference between Gradio and Streamlit"},
    ],
    run_examples_on_click=False,
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
