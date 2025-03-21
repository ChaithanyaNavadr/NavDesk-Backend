from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.core.dependencies import role_required, get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from typing import List
from passlib.context import CryptContext  # ✅ Import passlib for password hashing

router = APIRouter(prefix="/tenants/{tenant_id}/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Create User (Admin Only)
# @router.post("/", response_model=UserResponse, status_code=201)
# def create_user(
#     tenant_id: UUID,
#     user: UserCreate,
#     db: Session = Depends(get_db),
#     admin: User = Depends(role_required(["Admin"]))  # ✅ Only Admins can create users
# ):
#     # ✅ Hash the password before storing it
#     hashed_password = User.hash_password(user.password)

#     # ✅ Create user with hashed password
#     new_user = User(**user.model_dump(exclude={"password"}), password=hashed_password, tenant_id=tenant_id)

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    tenant_id: UUID,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    # ✅ Hash the password before storing it
    hashed_password = User.hash_password(user.password)

    # ✅ Create user with hashed password
    new_user = User(**user.model_dump(exclude={"password"}), password=hashed_password, tenant_id=tenant_id)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ✅ Get Current User Profile (Any Authenticated User)
@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


# ✅ Get All Users (Admin Only)
@router.get("/", response_model=List[UserResponse])
def get_users(
    tenant_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required(["Admin"]))  # ✅ Only Admins can get users
):
    return db.query(User).filter(User.tenant_id == tenant_id).all()


# ✅ Update User (Admin Only)
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    tenant_id: UUID,
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required(["Admin"]))  # ✅ Only Admins can update users
):
    user = db.query(User).filter(User.user_id == user_id, User.tenant_id == tenant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


# ✅ Delete User (Admin Only)
@router.delete("/{user_id}", status_code=204)
def delete_user(
    tenant_id: UUID,
    user_id: UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required(["Admin"]))  # ✅ Only Admins can delete users
):
    user = db.query(User).filter(User.user_id == user_id, User.tenant_id == tenant_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return
