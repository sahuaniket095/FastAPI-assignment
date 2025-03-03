from fastapi import FastAPI
from database import engine, Base, SessionLocal, get_db
from routes import auth, admin, participant
from models.user import User, Role
from utils.security import get_password_hash
from models.quiz import Quiz
from models.question import Question
from sqlalchemy.orm import Session

app = FastAPI()

# Including all routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(participant.router)

# Creating all tables
Base.metadata.create_all(bind=engine)
