from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.modules.equipment_photos import (
    service
)

router = APIRouter(
    prefix="/api/equipment-photos",
    tags=["Equipment Photos"]
)


@router.get("/{equipment_id}")
async def get_photos(
    equipment_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await service.get_equipment_photos(
        db,
        equipment_id
    )


@router.post("/{equipment_id}")
async def upload_photo(
    equipment_id: UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    return await service.upload_photo(
        db,
        equipment_id,
        file
    )


@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await service.delete_photo(
        db,
        photo_id
    )