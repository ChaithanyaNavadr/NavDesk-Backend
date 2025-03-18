from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.ticket_transfer import TicketTransfer
from app.schemas.ticket_transfer import TicketTransferCreate, TicketTransferResponse

router = APIRouter(
    prefix="/ticket-transfers",
    tags=["Ticket Transfers"]
)

# ✅ Create a new ticket transfer
@router.post("/", response_model=TicketTransferResponse)
def create_ticket_transfer(transfer_data: TicketTransferCreate, db: Session = Depends(get_db)):
    new_transfer = TicketTransfer(
        ticket_id=transfer_data.ticket_id,
        from_assignee=transfer_data.from_assignee,
        to_assignee=transfer_data.to_assignee,
        transfer_date=transfer_data.transfer_date
    )
    db.add(new_transfer)
    db.commit()
    db.refresh(new_transfer)
    return new_transfer

# ✅ Get all ticket transfers
@router.get("/", response_model=list[TicketTransferResponse])
def get_ticket_transfers(db: Session = Depends(get_db)):
    return db.query(TicketTransfer).all()

# ✅ Get a specific ticket transfer by ID
@router.get("/{transfer_id}", response_model=TicketTransferResponse)
def get_ticket_transfer(transfer_id: int, db: Session = Depends(get_db)):
    transfer = db.query(TicketTransfer).filter(TicketTransfer.transfer_id == transfer_id).first()
    if not transfer:
        raise HTTPException(status_code=404, detail="Ticket transfer not found")
    return transfer

# ✅ Delete a ticket transfer
@router.delete("/{transfer_id}")
def delete_ticket_transfer(transfer_id: int, db: Session = Depends(get_db)):
    transfer = db.query(TicketTransfer).filter(TicketTransfer.transfer_id == transfer_id).first()
    if not transfer:
        raise HTTPException(status_code=404, detail="Ticket transfer not found")

    db.delete(transfer)
    db.commit()
    return {"message": "Ticket transfer deleted successfully"}
