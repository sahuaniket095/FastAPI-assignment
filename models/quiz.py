# models/quiz.py
from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)               # Quiz title
    description = Column(String)         # Quiz description
    created_by = Column(Integer, ForeignKey("users.id"))  # ID of the admin who created it