from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from typing import List
from passlib.context import CryptContext  # ✅ Import passlib for password hashing


router = APIRouter(prefix="/tenants/{tenant_id}/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(tenant_id: int, user: UserCreate, db: Session = Depends(get_db)):
    # ✅ Hash the password before storing it
    hashed_password = User.hash_password(user.password)

    # ✅ Create user with hashed password
    new_user = User(**user.model_dump(exclude={"password"}), password=hashed_password, tenant_id=tenant_id)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/", response_model=List[UserResponse])
def list_users(tenant_id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.tenant_id == tenant_id).all()

@router.put("/{user_id}", response_model=UserResponse)
def update_user(tenant_id: int, user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def delete_user(tenant_id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return
 