from app.services.hvac import equipment_service
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.hvac.equipment import Equipment
from app.schemas.hvac.equipment import EquipmentCreate
from app.services.hvac import equipment_service
from app.services.hvac.equipment_service import (
    create_equipment,
    get_equipment_by_id
)
from uuid import UUID

router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"]
)


@router.post("/")
async def create_equipment_route(
    data: EquipmentCreate,
    db: AsyncSession = Depends(get_db)
):

    equipment = await create_equipment(
        db,
        data
    )

    return {
        "id": str(equipment.id),
        "asset_tag": equipment.asset_tag
    }


@router.get("/")
async def get_equipment(
    customer_id: str | None = None,
    location_id: str | None = None,
    db: AsyncSession = Depends(get_db)
):

    query = select(Equipment)

    if customer_id:
        query = query.where(
            Equipment.customer_id == customer_id
        )

    if location_id:
        query = query.where(
            Equipment.location_id == location_id
        )

    result = await db.execute(query)

    equipment = result.scalars().all()

    return [
        {
            "id": str(e.id),
            "asset_tag": e.asset_tag,
            "model": e.model
        }
        for e in equipment
    ]

@router.get("/{equipment_id}")
async def get_equipment_by_id_route(
    equipment_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await get_equipment_by_id(
        db,
        equipment_id
    )

@router.get("/{equipment_id}/qr")
async def get_equipment_qr_route(
    equipment_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await equipment_service.get_equipment_qr(
        db,
        equipment_id
    )

@router.get(
    "/equipment/{equipment_id}/intelligence"
)
async def equipment_intelligence(
    equipment_id: str,
    db=Depends(get_db)
):

    return {
        "health_score": 82,
        "maintenance_frequency": 14,
        "anomaly_risk": "High",
        "predicted_failure":
            "Compressor degradation risk",
        "refrigerant_events": 6,
        "component_failures": 3,
        "recent_failures": [

            {
                "component": "Compressor",
                "date": "2026-05-10",
                "severity": "Critical"
            },

            {
                "component": "Fan Motor",
                "date": "2026-04-18",
                "severity": "Medium"
            }
        ]
    }