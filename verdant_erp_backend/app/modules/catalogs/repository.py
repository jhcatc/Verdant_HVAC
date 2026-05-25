from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hvac import (
    Brand,
    EquipmentCategory,
    EquipmentStatus,
    EquipmentType,
    InstallationType,
    MaintenanceType,
    PowerSource,
    RefrigerantType,
    VoltageType
)


async def get_catalogs(
    db: AsyncSession
):

    equipment_categories = (
        await db.execute(
            select(
                EquipmentCategory
            ).order_by(
                EquipmentCategory.name
            )
        )
    ).scalars().all()

    equipment_types = (
        await db.execute(
            select(
                EquipmentType
            ).order_by(
                EquipmentType.name
            )
        )
    ).scalars().all()

    brands = (
        await db.execute(
            select(
                Brand
            ).order_by(
                Brand.name
            )
        )
    ).scalars().all()

    refrigerants = (
        await db.execute(
            select(
                RefrigerantType
            ).order_by(
                RefrigerantType.name
            )
        )
    ).scalars().all()

    voltages = (
        await db.execute(
            select(
                VoltageType
            ).order_by(
                VoltageType.name
            )
        )
    ).scalars().all()

    statuses = (
        await db.execute(
            select(
                EquipmentStatus
            ).order_by(
                EquipmentStatus.name
            )
        )
    ).scalars().all()

    installation_types = (
        await db.execute(
            select(
                InstallationType
            ).order_by(
                InstallationType.name
            )
        )
    ).scalars().all()

    power_sources = (
        await db.execute(
            select(
                PowerSource
            ).order_by(
                PowerSource.name
            )
        )
    ).scalars().all()

    maintenance_types = (
        await db.execute(
            select(
                MaintenanceType
            ).order_by(
                MaintenanceType.name
            )
        )
    ).scalars().all()

    return {
        "equipment_categories":
            equipment_categories,

        "equipment_types":
            equipment_types,

        "brands":
            brands,

        "refrigerants":
            refrigerants,

        "voltages":
            voltages,

        "statuses":
            statuses,

        "installation_types":
            installation_types,

        "power_sources":
            power_sources,

        "maintenance_types":
            maintenance_types
    }