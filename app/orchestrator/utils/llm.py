import ollama
from app.config import settings

def call_llm(prompt: str, model: str = None):
    """
    Calls a local Ollama model (e.g., llama3, mistral, phi3, etc.)
    """
    model = model or settings.LLM_MODEL
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"].strip()