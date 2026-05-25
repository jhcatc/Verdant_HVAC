import os
import uuid

from uuid import UUID

from fastapi import UploadFile

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hvac.equipment_document import (
    EquipmentDocument
)

from app.modules.equipment_documents import (
    repository
)

STORAGE_PATH = (
    "storage/equipment_documents"
)


async def upload_document(
    db: AsyncSession,
    equipment_id: UUID,
    maintenance_log_id: UUID | None,
    document_type: str | None,
    file: UploadFile
):

    os.makedirs(
        STORAGE_PATH,
        exist_ok=True
    )

    extension = (
        file.filename.split('.')[-1]
        if '.' in file.filename
        else ''
    )

    generated_name = (
        f'{uuid.uuid4()}.{extension}'
    )

    file_path = os.path.join(
        STORAGE_PATH,
        generated_name
    )

    content = await file.read()

    with open(
        file_path,
        'wb'
    ) as buffer:

        buffer.write(content)

    document = EquipmentDocument(

        equipment_id=equipment_id,

        maintenance_log_id=
            maintenance_log_id,

        file_name=file.filename,

        file_path=file_path,

        document_type=document_type
    )

    return await repository.create_document(
        db,
        document
    )


async def get_equipment_documents(
    db: AsyncSession,
    equipment_id: UUID
):

    return await repository.get_equipment_documents(
        db,
        equipment_id
    )


async def delete_document(
    db: AsyncSession,
    document_id: UUID
):

    document = await repository.get_document_by_id(
        db,
        document_id
    )

    if not document:

        return False

    if os.path.exists(
        document.file_path
    ):

        os.remove(
            document.file_path
        )

    await repository.delete_document(
        db,
        document
    )

    return True