import uuid
from sqlalchemy import String, Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base, metadata

role_permissions = Table(
    "role_permissions",
    metadata,
    Column("role_id", UUID(as_uuid=True), ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", UUID(as_uuid=True), ForeignKey("permissions.permission_id", ondelete="CASCADE"), primary_key=True),
    extend_existing=True  # ✅ Prevents redefinition error
)

class Permission(Base):
    __tablename__ = "permissions"

    permission_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_name = Column(String(100), unique=True, nullable=False)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions_rel")
