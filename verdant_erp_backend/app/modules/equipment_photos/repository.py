from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hvac.equipment_photo import (
    EquipmentPhoto
)


async def create_photo(
    db: AsyncSession,
    photo: EquipmentPhoto
):

    db.add(photo)

    await db.commit()

    await db.refresh(photo)

    return photo


async def get_equipment_photos(
    db: AsyncSession,
    equipment_id: UUID
):

    result = await db.execute(

        select(
            EquipmentPhoto
        ).where(
            EquipmentPhoto.equipment_id
            == equipment_id
        )
    )

    return result.scalars().all()


async def delete_photo(
    db: AsyncSession,
    photo: EquipmentPhoto
):

    await db.delete(photo)

    await db.commit()


async def get_photo_by_id(
    db: AsyncSession,
    photo_id: UUID
):

    result = await db.execute(

        select(
            EquipmentPhoto
        ).where(
            EquipmentPhoto.id == photo_id
        )
    )

    return result.scalars().first()