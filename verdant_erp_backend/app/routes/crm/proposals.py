from uuid import uuid4
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.crm.proposal import Proposal
from app.models.customer import Customer
from app.models.crm.opportunity import Opportunity
from app.schemas.crm.proposal_create import ProposalCreate
from app.schemas.crm.proposal_response import ProposalResponse
from app.services.crm.proposal_number import (
    generate_proposal_number
)


router = APIRouter(
    prefix="/crm/proposals",
    tags=["CRM Proposals"]
)


# =====================================================
# LIST
# =====================================================

@router.get(
    "/",
    response_model=list[ProposalResponse]
)
async def list_proposals(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Proposal).order_by(
            Proposal.created_at.desc()
        )
    )
    return result.scalars().all()


# =====================================================
# GET ONE
# =====================================================

@router.get(
    "/{proposal_id}",
    response_model=ProposalResponse
)
async def get_proposal(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):
    proposal = await db.get(
        Proposal,
        proposal_id
    )
    if not proposal:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found"
        )
    return proposal


# =====================================================
# CREATE
# =====================================================

@router.post(
    "/",
    response_model=ProposalResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_proposal(
    data: ProposalCreate,
    db: AsyncSession = Depends(get_db)
):

    # -------------------------------------------------
    # CUSTOMER REQUIRED
    # -------------------------------------------------

    customer = await db.get(
        Customer,
        data.customer_id
    )
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # -------------------------------------------------
    # OPTIONAL OPPORTUNITY
    # -------------------------------------------------

    source_type = "DIRECT"
    if data.opportunity_id:
        opportunity = await db.get(
            Opportunity,
            data.opportunity_id
        )
        if not opportunity:
            raise HTTPException(
                status_code=404,
                detail="Opportunity not found"
            )
        source_type = "PIPELINE"

    # -------------------------------------------------
    # GENERATE NUMBER
    # -------------------------------------------------

    proposal_number = (
        await generate_proposal_number(db)
    )

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------

    proposal = Proposal(
        id=uuid4(),
        proposal_number=proposal_number,
        customer_id=data.customer_id,
        opportunity_id=data.opportunity_id,
        source_type=source_type,
        title=data.title,
        status="DRAFT",
        amount=data.amount or 0,
        valid_until=data.valid_until
    )

    db.add(proposal)
    await db.commit()
    await db.refresh(proposal)
    return proposal


# =====================================================
# DELETE
# =====================================================

@router.delete(
    "/{proposal_id}"
)
async def delete_proposal(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):

    proposal = await db.get(
        Proposal,
        proposal_id
    )

    if not proposal:

        raise HTTPException(
            status_code=404,
            detail="Proposal not found"
        )

    await db.delete(proposal)
    await db.commit()
    return {
        "deleted": True
    }