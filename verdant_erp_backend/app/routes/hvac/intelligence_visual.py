from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.schemas.hvac.intelligence import (
    VisualIntelligenceSnapshotDTO
)
from app.services.hvac.intelligence.visual_intelligence_engine import (
    build_visual_intelligence_snapshot
)

router = APIRouter(
    prefix="/visual-intelligence",
    tags=["Visual Intelligence"]
)


@router.get(
    "/snapshot",
    response_model=VisualIntelligenceSnapshotDTO
)
async def snapshot(
    db=Depends(get_db)
):

    return await build_visual_intelligence_snapshot(db)