from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.catalogs import service
from app.modules.catalogs.schemas import (
    CatalogsResponseSchema
)

router = APIRouter()

@router.get(
    "/",
    response_model=CatalogsResponseSchema
)
async def get_catalogs(
    db: AsyncSession = Depends(get_db)
):
    return await service.get_catalogs(db)