from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.telemetry_service import ingest_telemetry

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


@router.post("/")
async def ingest(data: dict, db: AsyncSession = Depends(get_db)):

    await ingest_telemetry(db, data)

    await db.commit()

    return {"ok": True}