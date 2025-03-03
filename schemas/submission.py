from pydantic import BaseModel, Field
from typing import Dict, List
from datetime import datetime

class SubmissionCreate(BaseModel):
    quiz_id: int = Field(..., description="The ID of the quiz being submitted")
    answers: Dict[int, str] = Field(
        ...,
        description="A dictionary mapping question IDs to selected option letters (e.g., 'A', 'B', 'C', 'D')",
        example={1: "Correct Option", 2: "A"}  # Showing question ID: option
    )
    
class SubmissionOut(BaseModel):
    id: int
    quiz_id: int
    score: float
    submitted_at: datetime

    class Config:
        orm_mode = True

class AnswerResult(BaseModel):
    question_id: int
    selected_answer: str
    correct_answer: str

class SubmissionResult(BaseModel):
    score: float
    answers: List[AnswerResult]