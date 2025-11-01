import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    LLM_MODEL = os.getenv("LLM_MODEL", "phi3")  # any local ollama model
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/qdrant")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "knowledge_base")

settings = Settings()