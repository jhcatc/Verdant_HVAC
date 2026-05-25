from uuid import UUID
from fastapi import APIRouter


from app.modules.equipment_qr import (
    service
)

router = APIRouter(
    prefix="/api/equipment-qr",
    tags=["Equipment QR"]
)


@router.get("/{equipment_id}")
async def get_equipment_qr(
    equipment_id: UUID
):

    return service.generate_equipment_qr(
        equipment_id
    )

    