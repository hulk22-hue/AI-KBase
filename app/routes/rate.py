from fastapi import APIRouter
from pydantic import BaseModel, Field
import json, os
from datetime import datetime

router = APIRouter()

class RatingRequest(BaseModel):
    question: str
    answer: str
    rating: str = Field(..., pattern="^(like|dislike)$", description="User feedback: like or dislike")
    comments: str = ""

@router.post("/rate")
def rate_answer(req: RatingRequest):
    os.makedirs("./data/feedback", exist_ok=True)
    feedback = {
        "question": req.question,
        "answer": req.answer,
        "rating": req.rating,
        "comments": req.comments,
        "timestamp": datetime.utcnow().isoformat()
    }
    with open("./data/feedback/ratings.jsonl", "a") as f:
        f.write(json.dumps(feedback) + "\n")

    return {"message": "Feedback recorded successfully", "status": req.rating}