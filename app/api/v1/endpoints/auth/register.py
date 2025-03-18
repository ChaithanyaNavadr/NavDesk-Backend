# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.models.user import User
# from app.schemas.user import UserCreate
# from app.core.database import get_db

# router = APIRouter()

# @router.post("/register")
# def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
#     """Register a new user with hashed password"""
#     existing_user = db.query(User).filter(User.email == user_data.email).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = User.hash_password(user_data.password)  # ✅ Hash password
#     new_user = User(
#         email=user_data.email,
#         password=hashed_password,  # ✅ Store hashed password, but keep field name as "password"
#         first_name=user_data.first_name,
#         last_name=user_data.last_name,
#         tenant_id=user_data.tenant_id,
#         role_id=user_data.role_id
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "User registered successfully"}
