from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.services.maintenance.pm_generator_service import (
    generate_preventive_maintenance_orders
)

router = APIRouter(
    prefix="/maintenance/generator",
    tags=["maintenance-generator"]
)


@router.post("/run")
async def run_pm_generation(
    db: AsyncSession = Depends(get_db)
):

    return await generate_preventive_maintenance_orders(
        db
    )