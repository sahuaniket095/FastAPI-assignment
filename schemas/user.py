from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    """
    Enum to define different user roles.
    """
    admin = "admin"  # Role for administrators with full access
    participant = "participant"  # Role for regular users who can take quizzes

class UserCreate(BaseModel):
    """
    Model for user registration.
    """
    username: str  # Username of the user
    password: str  # Password for authentication (should be hashed before storing)
    role: Role  # Role assigned to the user (admin or participant)

class UserOut(BaseModel):
    """
    Model for returning user details after registration or login.
    """
    id: int  # Unique identifier for the user
    username: str  # Username of the user
    role: Role  # Role assigned to the user

    class Config:
        orm_mode = True  # Allows Pydantic to work with ORM objects like SQLAlchemy models

class Token(BaseModel):
    """
    Model for authentication tokens.
    """
    access_token: str  # The JWT token used for authentication
    token_type: str  # Type of the token (e.g., "Bearer")
