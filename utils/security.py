from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

# Secret key for JWT (replace with a more secure, environment-stored key in production)
SECRET_KEY = "ff5667dc669c6a3bb3e230abb6e7ffd0fdc4a75bbabbeaf1a76345f45ea749dc"
ALGORITHM = "HS256"

# Initialize a password hashing context using bcrypt
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for handling authentication token (used in dependency injection)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

# Function to hash a password before storing it in the database
def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

# Function to verify if a given plain password matches its hashed version
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

# Function to create a JWT access token for authentication
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta) -> str:
    # Create a dictionary with user details
    encode = {"sub": username, "id": user_id, "role": role}
    
    # Set the expiration time for the token
    expires = datetime.utcnow() + expires_delta
    encode["exp"] = expires  # Add expiration to the token payload
    
    # Encode the payload using the secret key and return the token
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to decode a JWT token and extract its payload
def decode_access_token(token: str):
    try:
        # Decode the token using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return decoded payload if valid
    except JWTError:
        return None  # Return None if the token is invalid or expired

# Dependency function to get the current authenticated user from the JWT token
async def get_current_user(token: str = Depends(oauth2_bearer)):
    # Decode the token
    payload = decode_access_token(token)
    
    # If token is invalid, raise an authentication error
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Extract user details from the payload
    username = payload.get("sub")
    user_id = payload.get("id")
    role = payload.get("role")
    
    # If required fields are missing, raise an error
    if not username or not user_id or not role:
        raise HTTPException(status_code=401, detail="Invalid token data")
    
    # Return user details
    return {"username": username, "id": user_id, "role": role}

# Dependency function to check if the user is an admin
async def get_current_admin(current_user: dict = Depends(get_current_user)):
    # If the user role is not admin, raise a permission error
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Must be an admin")
    
    return current_user  # Return user details if they are an admin

# Dependency function to check if the user is a participant
async def get_current_participant(current_user: dict = Depends(get_current_user)):
    # If the user role is not participant, raise a permission error
    if current_user["role"] != "participant":
        raise HTTPException(status_code=403, detail="Must be a participant")
    
    return current_user  # Return user details if they are a participant
