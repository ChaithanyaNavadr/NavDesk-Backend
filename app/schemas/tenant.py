from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TenantBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[bool] = True
    super_admin_id: Optional[int]  # ✅ Make sure this is present


class TenantCreate(TenantBase):
    pass

class TenantUpdate(TenantBase):
    pass

class TenantResponse(BaseModel):
    tenant_id: int  # ✅ Ensure this field matches your DB column
    name: str
    description: Optional[str] = None
    status: bool
    super_admin_id: Optional[int]  # ✅ Ensure this is included
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ Allows ORM conversion
