from uuid import UUID
from pydantic import BaseModel

class PermissionCreate(BaseModel):
    permission_name: str

class PermissionResponse(PermissionCreate):
    permission_id: UUID

    class Config:
        from_attributes = True
