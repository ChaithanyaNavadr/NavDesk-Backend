from pydantic import BaseModel

class CommentCreate(BaseModel):
    text: str
    ticket_id: int

class CommentResponse(CommentCreate):
    id: int

    class Config:
        from_attributes = True
