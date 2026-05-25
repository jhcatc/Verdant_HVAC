from uuid import UUID

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hvac.equipment_document import (
    EquipmentDocument
)


async def create_document(
    db: AsyncSession,
    document: EquipmentDocument
):

    db.add(document)

    await db.commit()

    await db.refresh(document)

    return document


async def get_equipment_documents(
    db: AsyncSession,
    equipment_id: UUID
):

    result = await db.execute(

        select(
            EquipmentDocument
        )
        .where(
            EquipmentDocument.equipment_id
            == equipment_id
        )
        .order_by(
            EquipmentDocument.uploaded_at.desc()
        )
    )

    return result.scalars().all()


async def get_document_by_id(
    db: AsyncSession,
    document_id: UUID
):

    result = await db.execute(

        select(
            EquipmentDocument
        )
        .where(
            EquipmentDocument.id
            == document_id
        )
    )

    return result.scalars().first()


async def delete_document(
    db: AsyncSession,
    document: EquipmentDocument
):

    await db.delete(document)

    await db.commit()