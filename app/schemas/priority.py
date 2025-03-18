from pydantic import BaseModel

class PriorityCreate(BaseModel):
    priority_name: str
    priority_level: int

class PriorityUpdate(PriorityCreate):
    pass

class PriorityResponse(PriorityCreate):
    priority_id: int

    class Config:
        from_attributes = True
