from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, query, rate

app = FastAPI(title="AI Knowledge Base Search & Enrichment")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(query.router, prefix="/api")
app.include_router(rate.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI-Powered Knowledge Base running!"}