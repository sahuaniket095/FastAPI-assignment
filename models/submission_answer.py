# models/submission_answer.py
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class SubmissionAnswer(Base):
    __tablename__ = "submission_answers"
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id")) # Link to submission
    question_id = Column(Integer, ForeignKey("questions.id"))     # Link to question
    selected_answer = Column(String)                              # Participant's answer (e.g., "B")