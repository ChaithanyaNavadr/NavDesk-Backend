from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_active: bool = True

class ProductUpdate(ProductCreate):
    pass

class ProductResponse(ProductCreate):
    product_id: int

    class Config:
        from_attributes = True
