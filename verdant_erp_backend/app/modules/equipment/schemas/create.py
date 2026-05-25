from pydantic import BaseModel

class EquipmentCreateSchema(
    BaseModel
):

    asset_tag: str
    model: str | None = None
    brand_id: int | None = None
    equipment_type_id: int | None = None
    equipment_status_id: int | None = None