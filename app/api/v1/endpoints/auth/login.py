from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import Token, LoginRequest

router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Function to create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(hours=1))
    to_encode.update({"exp": expire})  # Add expiration time
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

@router.post("/login", response_model=Token)
def login_for_access_token(user_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user with username and password, return JWT token including tenant_id.
    """
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ✅ Store `user_id` and `tenant_id` in token
    access_token = create_access_token(
        data={"sub": str(user.user_id), "tenant_id": user.tenant_id}
    )
    import json

# ✅ Print encoded token and payload
    print("Generated Token:", access_token)
    decoded_payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
    print("Decoded Payload:", json.dumps(decoded_payload, indent=4))

    return {"access_token": access_token, "token_type": "bearer"}
