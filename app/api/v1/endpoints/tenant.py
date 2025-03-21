from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from typing import List

router = APIRouter(prefix="/tenants", tags=["Tenants"])

# ✅ Create a new tenant
@router.post("/", response_model=TenantResponse, status_code=201)
def create_tenant(tenant_data: TenantCreate, db: Session = Depends(get_db)):
    new_tenant = Tenant(**tenant_data.model_dump())
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    return new_tenant

# ✅ Get all tenants
@router.get("/", response_model=List[TenantResponse])
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()

# ✅ Get a specific tenant by UUID
@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(tenant_id: UUID, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return tenant

# ✅ Update a tenant
@router.put("/{tenant_id}", response_model=TenantResponse)
def update_tenant(tenant_id: UUID, tenant_data: TenantUpdate, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    for key, value in tenant_data.model_dump(exclude_unset=True).items():
        setattr(tenant, key, value)

    db.commit()
    db.refresh(tenant)
    return tenant

# ✅ Delete a tenant
@router.delete("/{tenant_id}", status_code=204)
def delete_tenant(tenant_id: UUID, db: Session = Depends(get_db)):
    tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")

    db.delete(tenant)
    db.commit()
    return
