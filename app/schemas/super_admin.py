from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class SuperAdminBase(BaseModel):
    name: str
    email: EmailStr

class SuperAdminCreate(SuperAdminBase):
    password: str

class SuperAdminResponse(SuperAdminBase):
    super_admin_id: int
    created_at: datetime

    class Config:
        from_attributes = True
