from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class RoleBase(BaseModel):
    name: str
    # permissions: List[str]
    description: Optional[str] = None

class RoleCreate(RoleBase):
    name: str
    description: Optional[str] = None

class RoleUpdate(RoleBase):
    pass

class RoleResponse(BaseModel):
    role_id: UUID  # ✅ Updated to UUID
    name: str
    # permissions: List[str]
    description: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ Ensure it works with SQLAlchemy models
