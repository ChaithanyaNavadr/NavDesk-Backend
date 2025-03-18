from pydantic import BaseModel
from datetime import datetime

class StatusCreate(BaseModel):
    name: str

class StatusUpdate(BaseModel):
    name: str

class StatusResponse(StatusCreate):
    status_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
