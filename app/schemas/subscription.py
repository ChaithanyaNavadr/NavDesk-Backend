from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ✅ Schema for creating a subscription
class SubscriptionCreate(BaseModel):
    tenant_id: UUID
    product_id: UUID
    start_date: datetime
    end_date: datetime

# ✅ Schema for updating a subscription
class SubscriptionUpdate(BaseModel):
    tenant_id: Optional[UUID] = None
    product_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

# ✅ Schema for returning subscription data
class SubscriptionResponse(BaseModel):
    subscription_id: UUID
    tenant_id: UUID
    product_id: int
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True  # ✅ Enables ORM compatibility
