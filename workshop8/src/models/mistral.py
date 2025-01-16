import os

from huggingface_hub import hf_hub_download
from langchain.llms import LlamaCpp, Bedrock, gpt4all, Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from models.base import BaseModel


class MistralModel(BaseModel):
    def __init__(self, model_path: str):
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.model = LlamaCpp(
            model_path=model_path,
            temperature=0.3,
            max_tokens=8000,
            n_ctx=8048,
            callback_manager=callback_manager,
            
            n_gpu_layers=35,
            verbose=True,
        )

    def _ensure_model(self, model_path: str) -> str:
        if os.path.exists(model_path):
            return model_path

        print(f"Model not found at {model_path}. Downloading from Hugging Face...")
        repo_id = "MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF"
        filename = "Mistral-7B-Instruct-v0.3.Q8_0.gguf"

        download_path = hf_hub_download(repo_id=repo_id, filename=filename)
        print(f"Model downloaded to {download_path}")

        return download_path

    def generate(self, prompt: str) -> str:
        return self.model(prompt)

    def get_llm(self) -> LlamaCpp:
        return self.model
