# models/submission.py
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from database import Base
from datetime import datetime

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))    # Participant who submitted
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))  # Quiz submitted
    score = Column(Float)                                # Calculated score (percentage)
    submitted_at = Column(DateTime, default=datetime.utcnow)  # Submission timestamp