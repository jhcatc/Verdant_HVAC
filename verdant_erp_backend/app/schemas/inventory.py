from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class InventoryItemCreate(BaseModel):
    name: str
    sku: Optional[str] = None
    category: Optional[str] = "material"
    unit_cost: Optional[float] = 0
    stock: Optional[float] = 0


class InventoryItemOut(BaseModel):
    id: UUID   # 👈 CAMBIO AQUÍ
    name: str
    sku: Optional[str]
    category: Optional[str]
    unit_cost: Optional[float]
    stock: Optional[float]

    class Config:
        from_attributes = True
        from_attributes = True


class InventoryItemResponse(BaseModel):
    id: str
    name: str
    stock: float
    unit_cost: float
    category: str

    class Config:
        from_attributes = True