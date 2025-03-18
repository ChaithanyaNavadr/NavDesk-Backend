from pydantic import BaseModel
from datetime import datetime

class SubscriptionCreate(BaseModel):
    user_id: int
    product_id: int
    start_date: datetime
    end_date: datetime

class SubscriptionUpdate(SubscriptionCreate):
    pass

class SubscriptionResponse(SubscriptionCreate):
    subscription_id: int

    class Config:
        from_attributes = True
