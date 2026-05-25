from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.schemas.hvac.intelligence import (
    IntelligenceSnapshotDTO,
    CorrelationSnapshotDTO
)
from app.services.hvac.intelligence.engine import (
    build_intelligence_snapshot
)
from app.services.hvac.intelligence.service_intelligence_engine import (
    build_service_intelligence_snapshot
)
from app.services.hvac.intelligence.correlation_engine import (
    build_correlation_snapshot
)

router = APIRouter(
    prefix="/intelligence",
    tags=["Infrastructure Intelligence"]
)


@router.get(
    "/snapshot",
    response_model=IntelligenceSnapshotDTO
)
async def get_snapshot(
    db=Depends(get_db)
):

    infrastructure = (
        await build_intelligence_snapshot(db)
    )

    service = (
        await build_service_intelligence_snapshot(db)
    )

    return {
        "infrastructure": infrastructure,
        "service": service
    }


@router.get(
    "/correlation",
    response_model=CorrelationSnapshotDTO
)
async def correlation(
    db=Depends(get_db)
):

    return await build_correlation_snapshot(db)

@router.get("/clusters")
async def clusters(
    db=Depends(get_db)
):

    return await build_cluster_snapshot(db)