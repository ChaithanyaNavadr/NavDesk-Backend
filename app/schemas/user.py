from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# ✅ Base Schema for User (shared fields)
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role_id: int
    mobile_no: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_size: Optional[str] = None
    status: Optional[bool] = True

# ✅ Schema for Creating a User (includes password)
class UserCreate(UserBase):
    password: str  # ✅ Accepts password input for new users

# ✅ Schema for Updating a User (allows partial updates)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role_id: Optional[int] = None
    mobile_no: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_size: Optional[str] = None
    status: Optional[bool] = None

# ✅ Schema for Response (excludes password for security)
class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ Enable ORM Mode for SQLAlchemy
