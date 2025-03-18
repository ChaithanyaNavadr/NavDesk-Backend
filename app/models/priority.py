from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Priority(Base):
    __tablename__ = "priorities"

    priority_id = Column(Integer, primary_key=True, autoincrement=True)
    priority_name = Column(String(50), unique=True, nullable=False, index=True)
    priority_level = Column(Integer, unique=True, nullable=False)

    # ✅ Relationship with Ticket
    tickets = relationship("Ticket", back_populates="priority")
