from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionResponse

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)

# ✅ Create a new permission
@router.post("/", response_model=PermissionResponse)
def create_permission(permission_data: PermissionCreate, db: Session = Depends(get_db)):
    existing_permission = db.query(Permission).filter(Permission.permission_name == permission_data.permission_name).first()
    if existing_permission:
        raise HTTPException(status_code=400, detail="Permission already exists")

    new_permission = Permission(permission_name=permission_data.permission_name)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

# ✅ Get all permissions
@router.get("/", response_model=list[PermissionResponse])
def get_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()

# ✅ Get a specific permission by ID
@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.permission_id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

# ✅ Update a permission
@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(permission_id: int, permission_data: PermissionCreate, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.permission_id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    permission.permission_name = permission_data.permission_name
    db.commit()
    db.refresh(permission)
    return permission

# ✅ Delete a permission
@router.delete("/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(Permission).filter(Permission.permission_id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(permission)
    db.commit()
    return {"message": "Permission deleted successfully"}
