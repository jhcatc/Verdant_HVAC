from pydantic import BaseModel


class EquipmentCatalogResponse(BaseModel):
    id: str
    sku: str
    manufacturer: str
    model_number: str
    name: str
    category: str
    equipment_cost: float
    equipment_price: float

    class Config:
        from_attributes = True