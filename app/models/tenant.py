import uuid
from sqlalchemy.dialects.postgresql import UUID  # ✅ Use dialect-specific UUID
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), default="active", nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Foreign Key linking to SuperAdmin
    super_admin_id = Column(Integer, ForeignKey("super_admins.super_admin_id"), nullable=False)

    # Relationship with SuperAdmin
    super_admin = relationship("SuperAdmin", back_populates="tenants")

    users = relationship("User", back_populates="tenant")
    subscriptions = relationship("Subscription", back_populates="tenant")  # ✅ Link to subscriptions
