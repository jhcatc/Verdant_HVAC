from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    HTTPException
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.modules.equipment_documents import (
    service
)

router = APIRouter(
    prefix="/api/equipment-documents",
    tags=["Equipment Documents"]
)


@router.get("/{equipment_id}")
async def get_equipment_documents(
    equipment_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    return await service.get_equipment_documents(
        db,
        equipment_id
    )


@router.post("/")
async def upload_document(
    equipment_id: UUID = Form(...),
    maintenance_log_id: UUID | None = Form(None),
    document_type: str | None = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):

    return await service.upload_document(
        db,
        equipment_id,
        maintenance_log_id,
        document_type,
        file
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    deleted = await service.delete_document(
        db,
        document_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "success": True
    }