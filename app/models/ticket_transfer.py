from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class TicketTransfer(Base):
    __tablename__ = "ticket_transfers"

    transfer_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.ticket_id", ondelete="CASCADE"), nullable=False)
    from_assignee = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)  # Set NULL if user is deleted
    to_assignee = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"), nullable=True)  
    transfer_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    ticket = relationship("Ticket", back_populates="transfers")
    from_user = relationship("User", foreign_keys=[from_assignee])
    to_user = relationship("User", foreign_keys=[to_assignee])
