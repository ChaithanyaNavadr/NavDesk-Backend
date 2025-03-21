from uuid import UUID
from pydantic import BaseModel

class CommentCreate(BaseModel):
    text: str
    ticket_id: UUID

class CommentResponse(CommentCreate):
    comment_id: UUID

    class Config:
        from_attributes = True
