from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ✅ Request Schema for Creating a Ticket
class TicketCreate(BaseModel):
    title: str
    description: str
    priority_id: int
    status_id: int

    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy

class TicketUpdate(BaseModel):
    pass

# ✅ Response Schema for Returning Ticket Data
class TicketResponse(BaseModel):
    ticket_id: int
    title: str
    description: str
    user_id: int  # Extracted from JWT token
    priority_id: int
    status_id: int
    created_at: datetime  # Auto-generated timestamp

    class Config:
        from_attributes = True  # Enables ORM mode for SQLAlchemy
