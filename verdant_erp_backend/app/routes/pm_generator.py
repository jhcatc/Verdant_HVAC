from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.services.pm_generation_service import (
    generate_pm_work_orders
)

router = APIRouter(
    prefix="/pm-generator",
    tags=["PM Generator"]
)


@router.post("/run")
async def run_pm_generator(
    db: AsyncSession = Depends(get_db)
):

    return await generate_pm_work_orders(db)