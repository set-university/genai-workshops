import tempfile
from pathlib import Path

import gradio as gr
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

LANGUAGES = {
    "English": {"code": "en", "system": "Respond in English."},
    "Ukrainian": {"code": "uk", "system": "Відповідай українською мовою."},
    "Spanish": {"code": "es", "system": "Responde en español."},
    "French": {"code": "fr", "system": "Réponds en français."},
    "German": {"code": "de", "system": "Antworte auf Deutsch."},
    "Polish": {"code": "pl", "system": "Odpowiadaj po polsku."},
    "Japanese": {"code": "ja", "system": "日本語で答えてください。"},
}


def transcribe_audio(audio_tuple, language):
    """Send recorded audio to Whisper and return the transcript."""
    if audio_tuple is None:
        return "", ""

    sr, audio_data = audio_tuple

    if audio_data.dtype != np.int16:
        if np.issubdtype(audio_data.dtype, np.floating):
            audio_data = (audio_data * 32767).astype(np.int16)
        else:
            audio_data = audio_data.astype(np.int16)

    import wave
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, "wb") as wf:
        channels = 1 if audio_data.ndim == 1 else audio_data.shape[1]
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_data.tobytes())

    lang_code = LANGUAGES.get(language, LANGUAGES["English"])["code"]

    with open(tmp.name, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", file=f, language=lang_code,
        )

    Path(tmp.name).unlink(missing_ok=True)
    return transcript.text, ""


def respond(user_text, history, language):
    """Generate a streaming chat response via GPT-4o, then speak it with TTS."""
    if not user_text.strip():
        yield history, None
        return

    lang_instruction = LANGUAGES.get(language, LANGUAGES["English"])["system"]

    history = history + [
        {"role": "user", "content": user_text},
        {"role": "assistant", "content": ""},
    ]

    messages = [
        {"role": "system", "content": f"You are a helpful voice assistant. Keep your answers concise (2-3 sentences) since they will be spoken aloud. {lang_instruction}"},
    ] + [{"role": h["role"], "content": h["content"]} for h in history[:-1]]

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
        max_tokens=300,
    )

    full_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            full_response += delta
            history[-1]["content"] = full_response
            yield history, None

    tts = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=full_response,
    )

    tmp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp_audio.write(tts.content)
    tmp_audio.close()

    yield history, tmp_audio.name


with gr.Blocks(title="Voice Assistant") as demo:
    gr.Markdown("# Voice Assistant\nSpeak into your microphone or type — the AI responds with text and voice.")

    chatbot = gr.Chatbot(height=400)

    with gr.Row():
        mic = gr.Audio(sources=["microphone"], label="Record", type="numpy")
        text_input = gr.Textbox(label="Or type here", placeholder="Type your message...", scale=3)
        lang = gr.Dropdown(choices=list(LANGUAGES.keys()), value="English", label="Language", scale=1)

    audio_out = gr.Audio(label="AI Response (audio)", autoplay=True, visible=True)

    transcript_box = gr.Textbox(visible=False)

    mic.stop_recording(
        fn=transcribe_audio,
        inputs=[mic, lang],
        outputs=[text_input, transcript_box],
    ).then(
        fn=respond,
        inputs=[text_input, chatbot, lang],
        outputs=[chatbot, audio_out],
    )

    text_input.submit(
        fn=respond,
        inputs=[text_input, chatbot, lang],
        outputs=[chatbot, audio_out],
    ).then(
        fn=lambda: "",
        outputs=[text_input],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7861, share=True)
