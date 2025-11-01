from fastapi import FastAPI
from app.routes import upload, query

app = FastAPI(title="AI Knowledge Base Search & Enrichment")

app.include_router(upload.router, prefix="/api")
app.include_router(query.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI-Powered Knowledge Base running!"}