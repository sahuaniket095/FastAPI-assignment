from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    participant = "participant"

class UserCreate(BaseModel):
    username: str
    password: str
    role: Role

class UserOut(BaseModel):
    id: int
    username: str
    role: Role

    class Config:
        orm_mode = True  # Permission for returning SQLAlchemy models directly

class Token(BaseModel):
    access_token: str
    token_type: str