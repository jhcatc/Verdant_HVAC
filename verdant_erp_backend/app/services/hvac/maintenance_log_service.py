from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.hvac.maintenance_log import MaintenanceLog
from app.models.hvac.equipment_measurement import EquipmentMeasurement
from app.models.hvac.equipment_component import EquipmentComponent

from app.schemas.hvac.maintenance_log import MaintenanceLogCreate


async def create_maintenance_log(
    db: AsyncSession,
    data: MaintenanceLogCreate,
    technician_id
):
    log = MaintenanceLog(
        equipment_id=data.equipment_id,
        technician_id=technician_id,
        maintenance_type_id=data.maintenance_type_id,
        notes=data.notes,
        equipment_condition=data.equipment_condition,
        refrigerant_added=data.refrigerant_added
    )

    db.add(log)

    await db.flush()

    for m in data.measurements:
        measurement = EquipmentMeasurement(
            maintenance_log_id=log.id,
            measurement_type=m.measurement_type,
            value=m.value,
            unit=m.unit
        )

        db.add(measurement)

    await db.commit()

    await db.refresh(log)

    return log


async def get_equipment_maintenance_logs(
    db: AsyncSession,
    equipment_id
):
    result = await db.execute(
        select(MaintenanceLog)
        .where(MaintenanceLog.equipment_id == equipment_id)
        .options(
            selectinload(MaintenanceLog.technician),
            selectinload(MaintenanceLog.maintenance_type),
            selectinload(MaintenanceLog.measurements),
        )
        .order_by(MaintenanceLog.created_at.desc())
    )

    return result.scalars().all()