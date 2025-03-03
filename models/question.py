from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from database import Base

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))  # Quiz linking
    statement = Column(String)                           # Text of question
    options = Column(JSON)                               # Options as JSON 
    correct_answer = Column(String)                      # Correct answer