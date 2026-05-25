from fastapi import APIRouter
from fastapi import Depends
from app.core.database import get_db
from app.schemas.hvac.component_registry import (
    ComponentRegistrySnapshotDTO
)
from app.services.hvac.component_registry_service import (
    get_component_registry_snapshot
)

router = APIRouter(
    prefix="/component-registry",
    tags=["Component Registry"]
)


@router.get(
    "/snapshot",
    response_model=ComponentRegistrySnapshotDTO
)
async def snapshot(
    db=Depends(get_db)
):

    return await get_component_registry_snapshot(db)