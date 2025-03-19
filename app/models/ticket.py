from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.ticket_transfer import TicketTransfer # ✅ Import Transfer model

class Ticket(Base):
    __tablename__ = "tickets"

    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=False)

    ticket_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)

    status_id = Column(Integer, ForeignKey("status.status_id"), nullable=False)
    priority_id = Column(Integer, ForeignKey("priorities.priority_id"), nullable=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="tickets")
    comments = relationship("Comment", back_populates="ticket")
    status = relationship("Status", back_populates="tickets")
    priority = relationship("Priority", back_populates="tickets")
    
    # ✅ Ensure Transfer is imported above
    transfers = relationship("TicketTransfer", back_populates="ticket", cascade="all, delete-orphan")
