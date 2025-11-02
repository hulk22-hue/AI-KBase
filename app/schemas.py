from pydantic import BaseModel, Field
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

class AutoFetchedItem(BaseModel):
    query: str
    data: str

class QueryResponse(BaseModel):
    answer: str
    evidence: List[EvidenceItem]
    confidence: float
    completeness: str
    missing_info: Optional[List[Any]] = None
    enrichment_actions: Optional[List[EnrichmentItem]] = None
    auto_fetched_data: Optional[List[AutoFetchedItem]] = None
    orchestration_trace: List[str]
    
class RatingRequest(BaseModel):
    question: str
    answer: str
    rating: str = Field(..., pattern="^(like|dislike)$")
    comments: str = ""
