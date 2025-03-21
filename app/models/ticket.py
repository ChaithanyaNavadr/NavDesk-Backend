import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    ticket_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.tenant_id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    assign_to = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    status_id = Column(Integer, ForeignKey("status.status_id"), nullable=False)
    priority_id = Column(Integer, ForeignKey("priorities.priority_id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="tickets_created")
    assignee = relationship("User", foreign_keys=[assign_to], back_populates="tickets_assigned")
    status = relationship("Status", back_populates="tickets")
    priority = relationship("Priority", back_populates="tickets")
    comments = relationship("Comment", back_populates="ticket", cascade="all, delete-orphan")
    transfers = relationship("TicketTransfer", back_populates="ticket", cascade="all, delete-orphan")