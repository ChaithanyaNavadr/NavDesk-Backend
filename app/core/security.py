from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings

# Secret key and algorithm for JWT
SECRET_KEY = settings.SECRET_KEY  # Ensure you have this in `.env`
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generate a JWT access token with an expiration time.
    
    Args:
        data (dict): The payload containing user details.
        expires_delta (timedelta, optional): Expiry duration for the token.
    
    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default 15 min expiry

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
