import os
import uuid

from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hvac.equipment_photo import (
    EquipmentPhoto
)

from app.modules.equipment_photos import (
    repository
)

UPLOAD_DIR = "storage/equipment/photos"


async def upload_photo(
    db: AsyncSession,
    equipment_id: UUID,
    file: UploadFile
):

    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    extension = file.filename.split(".")[-1]

    generated_name = (
        f"{uuid.uuid4()}.{extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        generated_name
    )

    contents = await file.read()

    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(contents)

    photo = EquipmentPhoto(

        equipment_id=equipment_id,

        file_name=file.filename,

        file_path=file_path
    )

    return await repository.create_photo(
        db,
        photo
    )


async def get_equipment_photos(
    db: AsyncSession,
    equipment_id: UUID
):

    return await repository.get_equipment_photos(
        db,
        equipment_id
    )


async def delete_photo(
    db: AsyncSession,
    photo_id: UUID
):

    photo = await repository.get_photo_by_id(
        db,
        photo_id
    )

    if not photo:

        return None

    if os.path.exists(photo.file_path):

        os.remove(photo.file_path)

    await repository.delete_photo(
        db,
        photo
    )

    return True