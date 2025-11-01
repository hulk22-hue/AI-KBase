import os, pdfplumber, docx2txt
from app.orchestrator.utils.embeddings import Embedder
from app.orchestrator.utils.storage import VectorStore

def ingest_document(file_path: str):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif ext == ".docx":
        text = docx2txt.process(file_path)
    else:
        with open(file_path, "r") as f:
            text = f.read()

    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    embedder = Embedder("sentence-transformers/all-MiniLM-L6-v2")
    vectors = embedder.embed(chunks)
    store = VectorStore()
    metadatas = [{"doc_id": os.path.basename(file_path), "chunk_id": str(i)} for i in range(len(chunks))]
    store.add_documents(vectors, metadatas)
    return len(chunks)