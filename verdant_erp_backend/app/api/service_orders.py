from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.db import get_db
from app.services.service_order_service import dispatch_with_rebalance

router = APIRouter()


@router.patch("/service-orders/{order_id}/dispatch")
async def dispatch_order(
    order_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db)
):
    plan = await dispatch_with_rebalance(
        db,
        order_id=order_id,
        technician_id=payload.get("technician_id"),
        scheduled_at=datetime.fromisoformat(payload.get("scheduled_at")),
        duration_hours=payload.get("duration_hours", 1)
    )

    return {"plan": plan}