import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    new_role = Role(
        name=role.name,
        description=role.description,
        # permissions=role.permissions if role.permissions else []
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role  # ✅ Ensures FastAPI gets the correct fields

@router.get("/", response_model=List[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: UUID, role_data: RoleUpdate, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    for key, value in role_data.model_dump(exclude_unset=True).items():
        setattr(role, key, value)

    db.commit()
    db.refresh(role)
    return role

@router.delete("/{role_id}", status_code=204)
def delete_role(role_id: UUID, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.role_id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    db.delete(role)
    db.commit()
