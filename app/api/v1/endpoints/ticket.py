from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.models.priority import Priority
from app.models.status import Status
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse
from typing import List
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/tenants/{tenant_id}/tickets", tags=["Tickets"])

@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new ticket. `user_id` is taken from JWT token (`sub`).
    `priority_id` and `status_id` must be valid and exist in the database.
    """

    tenant_id = current_user.tenant_id
    user_id = current_user.user_id  # Extract user_id from JWT token

    # ✅ Check if priority_id and status_id exist in the database
    status = db.query(Status).filter(Status.status_id == ticket.status_id).first()
    priority = db.query(Priority).filter(Priority.priority_id == ticket.priority_id).first()

    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")

    # ✅ Create and Save Ticket
    new_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        tenant_id=tenant_id,
        user_id=user_id,
        priority_id=ticket.priority_id,
        status_id=ticket.status_id
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


@router.get("/", response_model=List[TicketResponse])
def list_tickets(tenant_id: UUID, db: Session = Depends(get_db)):
    return db.query(Ticket).filter(Ticket.tenant_id == tenant_id).all()

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(tenant_id: UUID, ticket_id: UUID, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id, Ticket.tenant_id == tenant_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(tenant_id: UUID, ticket_id: UUID, ticket_data: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id, Ticket.tenant_id == tenant_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    for key, value in ticket_data.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)
    return ticket

@router.delete("/{ticket_id}", status_code=204)
def delete_ticket(tenant_id: UUID, ticket_id: UUID, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id, Ticket.tenant_id == tenant_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()
    return
