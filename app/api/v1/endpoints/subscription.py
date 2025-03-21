import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.subscription import Subscription
from app.schemas.subscription import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from uuid import UUID

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"]
)

# ✅ Create a new subscription (Requires `tenant_id` & `product_id` in the request)
@router.post("/", response_model=SubscriptionResponse)
def create_subscription(subscription_data: SubscriptionCreate, db: Session = Depends(get_db)):
    new_subscription = Subscription(
        tenant_id=subscription_data.tenant_id,
        product_id=subscription_data.product_id,
        start_date=subscription_data.start_date,
        end_date=subscription_data.end_date
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

# ✅ Get all subscriptions
@router.get("/", response_model=list[SubscriptionResponse])
def get_subscriptions(db: Session = Depends(get_db)):
    return db.query(Subscription).all()

# ✅ Get a specific subscription by ID
@router.get("/{subscription_id}", response_model=SubscriptionResponse)
def get_subscription(subscription_id: UUID, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

# ✅ Update a subscription
@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(subscription_id: UUID, subscription_data: SubscriptionUpdate, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    subscription.tenant_id = subscription_data.tenant_id
    subscription.product_id = subscription_data.product_id
    subscription.start_date = subscription_data.start_date
    subscription.end_date = subscription_data.end_date

    db.commit()
    db.refresh(subscription)
    return subscription

# ✅ Delete a subscription
@router.delete("/{subscription_id}")
def delete_subscription(subscription_id: UUID, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    db.delete(subscription)
    db.commit()
    return {"message": "Subscription deleted successfully"}
