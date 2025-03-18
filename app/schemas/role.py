from pydantic import BaseModel
from typing import List, Optional

class RoleBase(BaseModel):
    name: str
    permissions: List[str]
    description: Optional[str] = None

class RoleCreate(RoleBase):
    name: str

class RoleUpdate(RoleBase):
    pass

class RoleResponse(BaseModel):
    role_id: int  # ✅ Match the database field exactly
    name: str
    permissions: List[str]
    description: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ Ensure it works with SQLAlchemy models
