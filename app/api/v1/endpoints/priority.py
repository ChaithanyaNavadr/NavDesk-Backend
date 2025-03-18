from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.priority import Priority
from app.schemas.priority import PriorityCreate, PriorityUpdate, PriorityResponse

router = APIRouter(
    prefix="/priorities",
    tags=["Priorities"]
)

# ✅ Create a new priority
@router.post("/", response_model=PriorityResponse)
def create_priority(priority_data: PriorityCreate, db: Session = Depends(get_db)):
    existing_priority = db.query(Priority).filter(
        (Priority.priority_name == priority_data.priority_name) |
        (Priority.priority_level == priority_data.priority_level)
    ).first()
    if existing_priority:
        raise HTTPException(status_code=400, detail="Priority name or level already exists")

    new_priority = Priority(
        priority_name=priority_data.priority_name,
        priority_level=priority_data.priority_level
    )
    db.add(new_priority)
    db.commit()
    db.refresh(new_priority)
    return new_priority

# ✅ Get all priorities
@router.get("/", response_model=list[PriorityResponse])
def get_priorities(db: Session = Depends(get_db)):
    return db.query(Priority).order_by(Priority.priority_level).all()

# ✅ Get a specific priority by ID
@router.get("/{priority_id}", response_model=PriorityResponse)
def get_priority(priority_id: int, db: Session = Depends(get_db)):
    priority = db.query(Priority).filter(Priority.priority_id == priority_id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")
    return priority

# ✅ Update a priority
@router.put("/{priority_id}", response_model=PriorityResponse)
def update_priority(priority_id: int, priority_data: PriorityUpdate, db: Session = Depends(get_db)):
    priority = db.query(Priority).filter(Priority.priority_id == priority_id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")

    # Ensure priority name and level remain unique
    existing_priority = db.query(Priority).filter(
        ((Priority.priority_name == priority_data.priority_name) |
         (Priority.priority_level == priority_data.priority_level)) &
        (Priority.priority_id != priority_id)
    ).first()

    if existing_priority:
        raise HTTPException(status_code=400, detail="Priority name or level already exists")

    priority.priority_name = priority_data.priority_name
    priority.priority_level = priority_data.priority_level

    db.commit()
    db.refresh(priority)
    return priority

# ✅ Delete a priority
@router.delete("/{priority_id}")
def delete_priority(priority_id: int, db: Session = Depends(get_db)):
    priority = db.query(Priority).filter(Priority.priority_id == priority_id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")

    db.delete(priority)
    db.commit()
    return {"message": "Priority deleted successfully"}
