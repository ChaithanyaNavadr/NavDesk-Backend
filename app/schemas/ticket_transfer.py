from pydantic import BaseModel
from datetime import datetime

class TicketTransferCreate(BaseModel):
    ticket_id: int
    from_assignee: int
    to_assignee: int
    transfer_date: datetime

class TicketTransferResponse(TicketTransferCreate):
    transfer_id: int

    class Config:
        from_attributes = True
