from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.super_admin import SuperAdminCreate, SuperAdminResponse
from app.models.super_admin import SuperAdmin
from app.models.tenant import Tenant
from app.utils.hashing import hash_password  # Assuming hash_password function is in utils
import uuid

router = APIRouter(prefix="/super_admin", tags=["Super Admin"])

def create_super_admin(db: Session, admin_data: SuperAdminCreate):
    new_admin = SuperAdmin(
        name=admin_data.name,
        email=admin_data.email,
        password_hash=hash_password(admin_data.password),
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@router.post("/", response_model=SuperAdminResponse)
def register_super_admin(admin_data: SuperAdminCreate, db: Session = Depends(get_db)):
    # Ensure super admin creation
    return create_super_admin(db, admin_data)

# You can add more endpoints as necessary.
