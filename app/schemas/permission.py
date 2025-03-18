from pydantic import BaseModel

class PermissionCreate(BaseModel):
    permission_name: str

class PermissionResponse(PermissionCreate):
    permission_id: int

    class Config:
        from_attributes = True
