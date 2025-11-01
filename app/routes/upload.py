from fastapi import APIRouter, UploadFile, File
import os
from app.orchestrator.agents.ingestion_agent import ingest_document

router = APIRouter()

@router.post("/upload")
def upload_doc(file: UploadFile = File(...)):
    save_path = f"./data/uploads/{file.filename}"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(file.file.read())

    num_chunks = ingest_document(save_path)
    return {"message": "File uploaded and indexed", "num_chunks": num_chunks}