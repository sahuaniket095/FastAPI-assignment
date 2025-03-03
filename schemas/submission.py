from pydantic import BaseModel, Field
from typing import Dict, List
from datetime import datetime

class SubmissionCreate(BaseModel):
    """
    Model for creating a new quiz submission.
    """
    quiz_id: int = Field(..., description="The ID of the quiz being submitted")
    answers: Dict[int, str] = Field(
        ..., 
        description="A dictionary mapping question IDs to selected option letters (e.g., 'A', 'B', 'C', 'D')",
        example={1: "Correct Option", 2: "A"}  # Showing question ID: option
    )

class SubmissionOut(BaseModel):
    """
    Model for representing the response after a successful quiz submission.
    """
    id: int  # Unique identifier for the submission
    quiz_id: int  # The ID of the quiz that was attempted
    score: float  # The calculated score of the submission
    submitted_at: datetime  # Timestamp of when the submission was made

    class Config:
        orm_mode = True  # Enables ORM support for compatibility with database models

class AnswerResult(BaseModel):
    """
    Model to represent the result of a single question attempt.
    """
    question_id: int  # The ID of the question
    selected_answer: str  # The answer chosen by the user
    correct_answer: str  # The correct answer for the question

class SubmissionResult(BaseModel):
    """
    Model to represent the final result of the quiz submission.
    """
    score: float  # Final score obtained by the user
    answers: List[AnswerResult]  # List of question-wise answer results
