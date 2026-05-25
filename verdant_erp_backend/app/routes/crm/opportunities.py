import uuid
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.crm.pipeline import require_transition
from app.models.customer import Customer
from app.models.crm.opportunity import Opportunity
from app.services.crm_contract_service import (
    create_contract_from_opportunity
)
from app.schemas.crm.opportunity_create import (
    OpportunityCreate
)
from app.schemas.crm.opportunity_response import (
    OpportunityResponse
)
from app.schemas.crm.opportunity_stage_update import (
    OpportunityStageUpdate
)
from app.schemas.crm.opportunity_stage_response import (
    OpportunityStageResponse
)
from app.schemas.common.delete_response import (
    DeleteResponse
)


router = APIRouter(
    prefix="/crm/opportunities",
    tags=["CRM Opportunities"]
)



# =========================================================
# MAPPER
# =========================================================

def serialize_opportunity(
    opportunity: Opportunity
) -> OpportunityResponse:

    return OpportunityResponse(
        id=str(opportunity.id),
        customer_id=str(opportunity.customer_id),
        customer_name=(
            opportunity.customer.name
            if opportunity.customer else None
        ),
        title=opportunity.title,
        stage=opportunity.stage,
        probability=opportunity.probability,
        estimated_value=float(
            opportunity.estimated_value or 0
        ),
        close_date=opportunity.close_date,
    )


# =========================================================
# LIST
# =========================================================

@router.get(
    "/",
    response_model=list[OpportunityResponse]
)
async def list_opportunities(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Opportunity)
        .options(
            selectinload(Opportunity.customer)
        )
        .order_by(Opportunity.close_date.desc())
    )

    rows = result.scalars().all()

    return [
        serialize_opportunity(o)
        for o in rows
    ]


# =========================================================
# GET ONE
# =========================================================

@router.get(
    "/{opportunity_id}",
    response_model=OpportunityResponse
)
async def get_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Opportunity)
        .options(
            selectinload(Opportunity.customer)
        )
        .where(
            Opportunity.id == opportunity_id
        )
    )

    opportunity = result.scalar_one_or_none()

    if not opportunity:

        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    return serialize_opportunity(
        opportunity
    )


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",     
    response_model=OpportunityResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_opportunity(
    data: OpportunityCreate,
    db: AsyncSession = Depends(get_db)
):

    # =====================================================
    # VALIDATE CUSTOMER
    # =====================================================

    customer = await db.get(
        Customer,
        data.customer_id
    )

    if not customer:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    # =====================================================
    # CREATE
    # =====================================================

    opportunity = Opportunity(

        id=uuid.uuid4(),
        customer_id=data.customer_id,
        title=data.title,
        stage=data.stage,
        estimated_value=data.estimated_value,
        probability=data.probability,
        close_date=data.close_date
    )

    db.add(opportunity)

    await db.commit()

    # IMPORTANT
    await db.refresh(opportunity)

    # IMPORTANT
    await db.refresh(
        opportunity,
        attribute_names=["customer"]
    )

    # RETURN SERIALIZED
    return serialize_opportunity(
        opportunity
    )


# =========================================================
# PATCH STAGE
# =========================================================

@router.patch(
    "/{opportunity_id}/stage",
    response_model=OpportunityStageResponse
)
async def change_stage(
    opportunity_id: str,
    data: OpportunityStageUpdate,
    db: AsyncSession = Depends(get_db)
):

    opportunity = await db.get(
        Opportunity,
        opportunity_id
    )

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    require_transition(
        opportunity.stage,
        data.stage
    )

    opportunity.stage = data.stage
    if data.stage == "WON":
        opportunity.probability = 100
        contract = await create_contract_from_opportunity(
            db,
            opportunity
        )

        await db.commit()

        return OpportunityStageResponse(
            id=str(opportunity.id),
            stage="WON",
            contract_created=True,
            contract_id=str(contract.id)
        )

    await db.commit()

    return OpportunityStageResponse(
        id=str(opportunity.id),
        stage=opportunity.stage,
        contract_created=False,
        contract_id=None
    )


# =========================================================
# DELETE
# =========================================================

@router.delete(
    "/{opportunity_id}",
    response_model=DeleteResponse
)
async def delete_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db)
):

    opportunity = await db.get(
        Opportunity,
        opportunity_id
    )

    if not opportunity:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found"
        )

    await db.delete(opportunity)
    await db.commit()
    return DeleteResponse(
        deleted=True
    )

@router.get("/search")
async def search_opportunities(
    q: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Opportunity)
        .where(
            or_(
                Opportunity.title.ilike(
                    f"%{q}%"
                ),
                Opportunity.company.ilike(
                    f"%{q}%"
                )
            )
        )
        .limit(15)
    )
    opportunities = result.scalars().all()
    return opportunities