from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# # JWT Config
# SECRET_KEY = settings.SECRET_KEY
# ALGORITHM = "HS256"

# def create_access_token(data: dict, expires_delta: timedelta = None):
#     """
#     Generate a JWT token containing user ID, email, and role_name.

#     Args:
#         data (dict): User details to encode in JWT.
#         expires_delta (timedelta, optional): Expiry duration for the token.

#     Returns:
#         str: Encoded JWT token.
#     """
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))  # Default 1 hour expiry
#     to_encode.update({"exp": expire})
    
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
