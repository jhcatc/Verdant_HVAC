from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.schemas.hvac.equipment_component import (
    EquipmentComponentCreate
)
from app.services.hvac import (
    equipment_component_service
)
from app.services.hvac.equipment_service import (
    get_equipment_components
)


router = APIRouter(
    prefix="/equipment",
    tags=["Equipment Components"]
)


@router.get("/{equipment_id}/components")
async def get_components_route(
    equipment_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await (
        equipment_component_service
        .get_equipment_components(
            db,
            equipment_id
        )
    )


@router.post("/{equipment_id}/components")
async def create_component_route(
    equipment_id: UUID,
    data: EquipmentComponentCreate,
    db: AsyncSession = Depends(get_db)
):
    return await (
        equipment_component_service
        .create_component(
            db,
            equipment_id,
            data
        )
    )

@router.get("/{equipment_id}/components")
async def get_equipment_components_route(
    equipment_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await get_equipment_components(
        db,
        equipment_id
    )