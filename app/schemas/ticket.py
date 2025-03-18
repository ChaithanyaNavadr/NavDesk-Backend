from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "Open"
    priority: Optional[str] = "Medium"

class TicketCreate(TicketBase):
    pass

class TicketUpdate(TicketBase):
    pass

class TicketResponse(TicketBase):
    id: int
    tenant_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
