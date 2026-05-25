from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class EquipmentDocumentResponseSchema(
    BaseModel
):

    id: UUID

    equipment_id: UUID

    maintenance_log_id: UUID | None

    file_name: str

    file_path: str

    document_type: str | None

    uploaded_at: datetime

    class Config:

        from_attributes = True