from pydantic import BaseModel
from typing import List, Optional, Any

class UploadResponse(BaseModel):
    message: str
    num_chunks: int

class QueryRequest(BaseModel):
    text: str

class EvidenceItem(BaseModel):
    doc_id: str
    chunk_id: str
    score: float

class EnrichmentItem(BaseModel):
    type: str
    label: str

class QueryResponse(BaseModel):
    answer: str
    evidence: List[EvidenceItem]
    confidence: float
    completeness: str
    missing_info: Optional[List[Any]] = None
    enrichment_actions: Optional[List[EnrichmentItem]] = None
    orchestration_trace: List[str]