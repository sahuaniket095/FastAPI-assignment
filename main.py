
from fastapi import FastAPI  
from database import engine, Base, SessionLocal, get_db  # Import database engine, base model, session, and dependency  
from routes import auth, admin, participant  # Import API route modules  
from models.user import User, Role  # Import user and role models  
from utils.security import get_password_hash  # Import password hashing utility  
from models.quiz import Quiz  # Import quiz model  
from models.question import Question  # Import question model  
from sqlalchemy.orm import Session  # Import SQLAlchemy session for database operations  

# Initialize FastAPI app  
app = FastAPI()  

# Include authentication, admin, and participant routes  
app.include_router(auth.router)  
app.include_router(admin.router)  
app.include_router(participant.router)  

# Create all tables in the database based on the defined SQLAlchemy models  
Base.metadata.create_all(bind=engine)  

