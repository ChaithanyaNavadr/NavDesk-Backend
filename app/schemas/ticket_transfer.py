from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class TicketTransferCreate(BaseModel):
    ticket_id: UUID
    from_assignee: UUID
    to_assignee: UUID
    transfer_date: datetime

class TicketTransferResponse(TicketTransferCreate):
    transfer_id: UUID

    class Config:
        from_attributes = True
