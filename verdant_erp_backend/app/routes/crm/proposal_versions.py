from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession
)
from sqlalchemy.orm import (
    selectinload
)
from app.core.database import get_db
from app.models.crm.proposal import Proposal
from app.models.crm.proposal_version import (
    ProposalVersion
)
from app.services.crm.proposal_version_service import (
    create_proposal_version
)

router = APIRouter(
    prefix="/crm/proposals",
    tags=["Proposal Versions"]
)


@router.post(
    "/{proposal_id}/versions"
)
async def snapshot_version(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Proposal)
        .options(
            selectinload(
                Proposal.line_items
            )
        )

        .where(
            Proposal.id == proposal_id
        )
    )

    proposal = result.scalar_one_or_none()

    if not proposal:

        raise HTTPException(
            status_code=404,
            detail="Proposal not found"
        )

    return await create_proposal_version(
        db,
        proposal
    )


@router.get(
    "/{proposal_id}/versions"
)
async def list_versions(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(

        select(ProposalVersion)

        .where(
            ProposalVersion.proposal_id
            == proposal_id
        )

        .order_by(
            ProposalVersion.version_number.desc()
        )
    )

    return result.scalars().all()


@router.get(
    "/{proposal_id}/versions/{version_id}"
)
async def get_version(
    proposal_id: str,
    version_id: str,
    db: AsyncSession = Depends(get_db)
):

    version = await db.get(
        ProposalVersion,
        version_id
    )

    if not version:

        raise HTTPException(
            status_code=404,
            detail="Version not found"
        )

    return version