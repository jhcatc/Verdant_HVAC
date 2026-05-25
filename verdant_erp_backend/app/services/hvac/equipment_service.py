from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.hvac.equipment import Equipment
from app.schemas.hvac.equipment import EquipmentCreate
from sqlalchemy.orm import selectinload
from app.models.hvac.equipment_component import (
    EquipmentComponent
)


async def create_equipment(
    db: AsyncSession,
    data: EquipmentCreate
):

    equipment = Equipment(**data.model_dump())
    db.add(equipment)
    await db.commit()
    await db.refresh(equipment)
    return equipment

async def get_equipment_by_id(
    db: AsyncSession,
    equipment_id
):
    result = await db.execute(

        select(Equipment)
        .options(

            selectinload(Equipment.customer),
            selectinload(Equipment.location),
            selectinload(Equipment.category),
            selectinload(Equipment.equipment_type),
            selectinload(Equipment.brand),
            selectinload(Equipment.equipment_status),
            selectinload(Equipment.refrigerant),
            selectinload(Equipment.voltage)

        )
        .where(Equipment.id == equipment_id)
    )

    return result.scalar_one_or_none()

async def get_equipment_qr(
    db: AsyncSession,
    equipment_id
):

    result = await db.execute(

        select(Equipment)
        .options(
            selectinload(Equipment.customer)
        )
        .where(
            Equipment.id == equipment_id
        )
    )

    equipment = result.scalar_one_or_none()

    if not equipment:

        return None

    return {

        "equipment_id":
            str(equipment.id),

        "asset_tag":
            equipment.asset_tag,

        "serial_number":
            equipment.serial_number,

        "customer":
            equipment.customer.name
            if equipment.customer
            else None,

        "url":
            f"/app/infrastructure/equipment/{equipment.id}"
    }

async def get_equipment_components(
    db: AsyncSession,
    equipment_id
):

    result = await db.execute(

        select(EquipmentComponent)
        .where(
            EquipmentComponent.equipment_id == equipment_id
        )
        .order_by(
            EquipmentComponent.created_at.desc()
        )

    )

    components = result.scalars().all()

    return [

        {
            "id": str(component.id),
            "component_name": component.component_name,
            "component_type": component.component_type,
            "manufacturer": component.manufacturer,
            "model_number": component.model_number,
            "serial_number": component.serial_number,
            "status": component.status,
            "is_critical": component.is_critical,
            "installation_date": (
                str(component.installation_date)
                if component.installation_date
                else None
            ),
            "warranty_expiration": (
                str(component.warranty_expiration)
                if component.warranty_expiration
                else None
            )
        }

        for component in components
    ]