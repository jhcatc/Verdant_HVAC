from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class EquipmentPhotoResponseSchema(
    BaseModel
):

    id: UUID

    equipment_id: UUID

    file_name: str

    file_path: str

    uploaded_at: datetime

    class Config:

        from_attributes = True