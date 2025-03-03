
from pydantic import BaseModel
from typing import List, Dict

# Schema for creating a new quiz
class QuizCreate(BaseModel):
    title: str  # Title of the quiz
    description: str  # Brief description of the quiz

# Schema for questions as seen by participants (hides the correct answer)
class QuestionParticipant(BaseModel):
    id: int  # Unique identifier for the question
    statement: str  # The question text
    options: Dict[str, str]  # Dictionary containing answer choices (e.g., {"A": "Option A", "B": "Option B"})
    quiz_id: int  # The ID of the quiz to which this question belongs

# Schema for returning quiz details (includes questions)
class QuizOut(BaseModel):
    id: int  # Unique ID of the quiz
    title: str  # Title of the quiz
    description: str  # Description of the quiz
    created_by: int  # ID of the user who created the quiz
    questions: List[QuestionParticipant] = []  # List of questions in the quiz

    # ORM mode enables Pydantic to work with ORM models like SQLAlchemy
    class Config:
        orm_mode = True
