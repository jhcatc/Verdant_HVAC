from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.deps import get_current_user

from app.schemas.hvac.maintenance_log import (
    MaintenanceLogCreate
)

from app.services.hvac.maintenance_log_service import (
    create_maintenance_log,
    get_equipment_maintenance_logs
)

router = APIRouter(
    prefix="/maintenance-logs",
    tags=["HVAC Maintenance Logs"]
)


@router.post("/")
async def create_log(
    data: MaintenanceLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await create_maintenance_log(
        db,
        data,
        current_user.id
    )


@router.get("/equipment/{equipment_id}")
async def get_logs(
    equipment_id: str,
    db: AsyncSession = Depends(get_db)
):
    logs = await get_equipment_maintenance_logs(
        db,
        equipment_id
    )

    return [
        {
            "id": str(log.id),
            "technician": log.technician.full_name,
            "maintenance_type": log.maintenance_type.name,
            "notes": log.notes,
            "equipment_condition": log.equipment_condition,
            "refrigerant_added": log.refrigerant_added,
            "created_at": log.created_at,
            "measurements": [
                {
                    "type": m.measurement_type,
                    "value": m.value,
                    "unit": m.unit
                }
                for m in log.measurements
            ],
            "components": [
                {
                    "component_name": c.component_name,
                    "status": c.status,
                    "notes": c.notes
                }
                for c in log.components
            ]
        }
        for log in logs
    ]