from fastapi import APIRouter, Depends
from app.services.hvac.anomaly.engine import detect_anomalies
from app.core.database import get_db

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])


@router.post("/run")
async def run_anomaly_detection(db=Depends(get_db)):

    tickets = await detect_anomalies(db)

    return {
        "created": len(tickets),
        "tickets": tickets
    }