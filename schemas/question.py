from pydantic import BaseModel
from typing import Dict

# Schema for creating a new question
class QuestionCreate(BaseModel):
    statement: str  # The text of the question
    options: Dict[str, str]  # Dictionary containing options (e.g., {"A": "Option 1", "B": "Option 2"})
    correct_answer: str  # The correct answer (e.g., "A" or "B")
    quiz_id: int  # The ID of the quiz this question belongs to

# Schema for returning a question as a response
class QuestionOut(BaseModel):
    id: int  # Unique ID of the question
    statement: str  # The text of the question
    options: Dict[str, str]  # Dictionary containing answer choices
    correct_answer: str  # The correct answer
    quiz_id: int  # The ID of the quiz this question is part of

    # Configuration for ORM compatibility
    class Config:
        orm_mode = True  # Enables compatibility with ORM models (e.g., SQLAlchemy)
