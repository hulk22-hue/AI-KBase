from app.orchestrator.utils.embeddings import Embedder
from app.orchestrator.utils.storage import VectorStore

def retrieve_documents(query: str):
    embedder = Embedder("sentence-transformers/all-MiniLM-L6-v2")
    vector = embedder.embed([query])[0]
    store = VectorStore()
    results = store.search(vector, limit=5)
    docs = [{"doc_id": r.payload["doc_id"], "chunk_id": r.payload["chunk_id"], "score": r.score} for r in results]
    context = " ".join([r.payload.get("text", "") for r in results])
    return docs, context