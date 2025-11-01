from fastapi import APIRouter
from app.schemas import QueryRequest, QueryResponse
from app.orchestrator.orchestrator import orchestrate_pipeline

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    result = orchestrate_pipeline(req.text)
    return result