from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

# Defining user roles as an Enum
class Role(enum.Enum):
    admin = "admin"
    participant = "participant"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Username which must be unique
    hashed_password = Column(String)                    # hashed password storing
    role = Column(Enum(Role))                           # Role will be admin or participant