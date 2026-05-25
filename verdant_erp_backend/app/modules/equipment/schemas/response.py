from pydantic import BaseModel

class EquipmentResponseSchema(
    BaseModel
):

    id: str
    asset_tag: str
    model: str | None = None
    brand: CatalogItemSchema | None = None
    status: CatalogItemSchema | None = None
    category: EquipmentCategorySchema | None = None