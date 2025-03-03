
from sqlalchemy import create_engine  # Import SQLAlchemy engine for database connection  
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # Import session maker and base class for ORM models  

# Database connection URL (Update password encoding for security)  
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Aniket1234@localhost/v1"

# Create a database engine that establishes the connection with PostgreSQL  
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory for handling database transactions  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for defining ORM models  
class Base(DeclarativeBase):  
    pass  # Used as a base for all ORM models  

# Dependency to get a database session  
def get_db():  
    db = SessionLocal()  # Create a new database session  
    try:  
        yield db  # Provide the session to the request handler  
    finally:  
        db.close()  # Close the session after the request is completed  
