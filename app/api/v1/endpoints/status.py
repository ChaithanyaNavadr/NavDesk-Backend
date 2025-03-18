from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.status import Status
from app.schemas.status import StatusCreate, StatusUpdate, StatusResponse

router = APIRouter()

# ✅ Create a new status
@router.post("/", response_model=StatusResponse)
def create_status(status_data: StatusCreate, db: Session = Depends(get_db)):
    existing_status = db.query(Status).filter(Status.name == status_data.name).first()
    if existing_status:
        raise HTTPException(status_code=400, detail="Status name already exists")

    new_status = Status(name=status_data.name)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status

# ✅ Get all statuses
@router.get("/", response_model=list[StatusResponse])
def get_statuses(db: Session = Depends(get_db)):
    return db.query(Status).order_by(Status.created_at).all()

# ✅ Get a specific status by ID
@router.get("/{status_id}", response_model=StatusResponse)
def get_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.status_id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status

# ✅ Update a status
@router.put("/{status_id}", response_model=StatusResponse)
def update_status(status_id: int, status_data: StatusUpdate, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.status_id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    existing_status = db.query(Status).filter(
        Status.name == status_data.name, Status.status_id != status_id
    ).first()
    if existing_status:
        raise HTTPException(status_code=400, detail="Status name already exists")

    status.name = status_data.name
    db.commit()
    db.refresh(status)
    return status

# ✅ Delete a status
@router.delete("/{status_id}")
def delete_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.status_id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    db.delete(status)
    db.commit()
    return {"message": "Status deleted successfully"}
