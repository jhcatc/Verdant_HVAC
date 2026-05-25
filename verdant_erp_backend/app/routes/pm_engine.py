from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.services.pm_generator_service import (
    run_pm_generation_engine
)

router = APIRouter(
    prefix="/pm-engine",
    tags=["PM Engine"]
)


@router.post("/run")
async def run_engine(
    db: AsyncSession = Depends(get_db)
):

    generated = await run_pm_generation_engine(db)

    return {
        "ok": True,
        "generated": len(generated)
    }