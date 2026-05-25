from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.crm.equipment_catalog import (
    EquipmentCatalog
)

router = APIRouter(
    prefix="/crm/equipment-catalog",
    tags=["Equipment Catalog"]
)


@router.get("/")
async def list_catalog(
    search: str | None = None,
    db: AsyncSession = Depends(get_db)
):

    query = select(
        EquipmentCatalog
    )

    if search:

        query = query.where(
            EquipmentCatalog.name.ilike(
                f"%{search}%"
            )
        )

    result = await db.execute(query)
    return result.scalars().all()