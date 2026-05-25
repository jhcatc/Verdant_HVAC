from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.services.sla_engine_service import (
    get_sla_dashboard
)

router = APIRouter(
    prefix="/sla-engine",
    tags=["SLA Engine"]
)


@router.get("/dashboard")
async def sla_dashboard(
    db: AsyncSession = Depends(get_db)
):

    return await get_sla_dashboard(db)