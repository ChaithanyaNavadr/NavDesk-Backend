from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    role_id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    mobile_no: Optional[str] = None
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    company_size: Optional[str] = None
    status: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # ✅ Enable ORM Mode for SQLAlchemy
        arbitrary_types_allowed = True  # ✅ Fix for UUID

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: UUID
    tenant_id: UUID


class UserUpdate(UserBase):
    pass