from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from passlib.context import CryptContext  # ✅ Import password hashing
from app.core.database import Base

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # ✅ Keeping attribute name as "password"
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    mobile_no = Column(String(15), nullable=True)
    job_title = Column(String(255), nullable=True)
    company_name = Column(String(255), nullable=True)
    company_size = Column(String(50), nullable=True)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    tenant = relationship("Tenant", back_populates="users")
    tickets = relationship("Ticket", back_populates="user")
    role = relationship("Role", back_populates="users")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")

    # ✅ Function to hash passwords before storing
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    # ✅ Function to verify passwords
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)
