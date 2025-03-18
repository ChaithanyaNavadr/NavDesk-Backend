from sqlalchemy import String, Table, Column, Integer, ForeignKey
from app.core.database import Base, metadata
from sqlalchemy.orm import relationship
role_permissions = Table(
    "role_permissions",
    metadata,
    Column("role_id", Integer, ForeignKey("roles.role_id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.permission_id", ondelete="CASCADE"), primary_key=True),
    extend_existing=True  # ✅ Prevents redefinition error
)

class Permission(Base):
    __tablename__ = "permissions"

    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    permission_name = Column(String(100), unique=True, nullable=False)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions_rel")
