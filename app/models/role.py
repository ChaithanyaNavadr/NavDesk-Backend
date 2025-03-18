from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB  # Use PostgreSQL's JSONB for better performance
from app.core.database import Base, metadata

# Many-to-Many Relationship Table (Role-Permission)
role_permissions = Table(
    "role_permissions",
    metadata,
    Column("role_id", Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.permission_id", ondelete="CASCADE"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    permissions = Column(JSONB, nullable=False, default=[])  # ✅ Set default to empty list
    description = Column(String(255), nullable=True)

    # Relationships
    users = relationship("User", back_populates="role")
    permissions_rel = relationship("Permission", secondary=role_permissions, back_populates="roles")
