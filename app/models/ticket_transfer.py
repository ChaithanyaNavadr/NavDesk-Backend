import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class TicketTransfer(Base):
    __tablename__ = "ticket_transfers"

    transfer_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False)
    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.ticket_id", ondelete="CASCADE"), nullable=False)
    from_assignee = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)  # Set NULL if user is deleted
    to_assignee = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)  
    transfer_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    ticket = relationship("Ticket", back_populates="transfers")
    from_user = relationship("User", foreign_keys=[from_assignee])
    to_user = relationship("User", foreign_keys=[to_assignee])
