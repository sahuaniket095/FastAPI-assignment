from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from models.user import User, Role
from schemas.user import UserCreate, UserOut, Token
from utils.security import get_password_hash, verify_password, create_access_token
from datetime import timedelta

# Creating an API router for authentication endpoints
router = APIRouter(prefix="/auth", tags=["auth"])

# ------------------- Registering a new user -------------------
@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - Checks if the username already exists.
    - Hashes the password before storing.
    - Saves the user to the database.
    """
    # Check if the username is already taken
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password before storing it
    hashed_password = get_password_hash(user.password)

    # Create a new user instance
    new_user = User(
        username=user.username, 
        hashed_password=hashed_password, 
        role=user.role  # Assign the role
    )

    db.add(new_user)  # Add the user to the database session
    db.commit()  # Commit changes to save the user
    db.refresh(new_user)  # Refresh the user instance

    return new_user  # Return the newly created user

# ------------------- Login and getting a JWT token -------------------
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Authenticate a user and generate a JWT token.
    - Checks if the user exists.
    - Verifies the provided password.
    - Generates an access token valid for 30 minutes.
    """
    # Fetch the user from the database using the provided username
    user = db.query(User).filter(User.username == form_data.username).first()

    # If the user does not exist or password is incorrect, return 401 error
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Create an access token valid for 30 minutes
    token = create_access_token(
        user.username,  # Username as the identity
        user.id,  # User ID
        user.role.value,  # User role
        timedelta(minutes=30)  # Token expiration time
    )

    # Return the generated token
    return {"access_token": token, "token_type": "bearer"}
