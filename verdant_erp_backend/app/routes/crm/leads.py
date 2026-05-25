from uuid import uuid4
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.lead import Lead
from app.models.crm.opportunity import Opportunity
from app.schemas.crm.lead_create import LeadCreate
from app.schemas.crm.lead_update import LeadUpdate
from app.schemas.crm.lead_response import LeadResponse
from app.schemas.crm.lead_detail_response import (
    LeadDetailResponse
)
from app.schemas.crm.lead_metrics_response import (
    LeadMetricResponse
)

router = APIRouter(
    prefix="/crm/leads",
    tags=["CRM Leads"]
)


# =========================================================
# LIST
# =========================================================

@router.get(
    "/",
    response_model=list[LeadResponse]
)
async def list_leads(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Lead)
    )

    leads = result.scalars().all()

    return [

        LeadResponse(
            id=l.id,
            contact_name=l.title,
            company_name=l.company,
            status=l.status,
            estimated_value=float(
                l.estimated_value or 0
            ),
            probability=l.probability or 0,
            source=l.source,
            assigned_rep=l.assigned_rep,
            city=l.city,
            email=l.email
        )

        for l in leads
    ]


# =========================================================
# METRICS
# =========================================================

@router.get(
    "/metrics",
    response_model=list[LeadMetricResponse]
)
async def lead_metrics(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Lead)
    )

    leads = result.scalars().all()

    open_leads = len(leads)

    qualified = len([

        l for l in leads

        if l.status == "QUALIFIED"
    ])

    pipeline_value = sum(

        float(l.estimated_value or 0)

        for l in leads
    )

    conversion_rate = (

        (qualified / open_leads) * 100

        if open_leads else 0
    )

    return [

        LeadMetricResponse(
            title="Open Leads",
            value=open_leads,
            color="text-emerald-400"
        ),

        LeadMetricResponse(
            title="Qualified",
            value=qualified,
            color="text-cyan-400"
        ),

        LeadMetricResponse(
            title="Pipeline Value",
            value=f"${pipeline_value:,.0f}",
            color="text-yellow-400"
        ),

        LeadMetricResponse(
            title="Conversion Rate",
            value=f"{conversion_rate:.1f}%",
            color="text-purple-400"
        )
    ]


# =========================================================
# GET ONE
# =========================================================

@router.get(
    "/{lead_id}",
    response_model=LeadDetailResponse
)
async def get_lead(
    lead_id: str,
    db: AsyncSession = Depends(get_db)
):

    lead = await db.get(
        Lead,
        lead_id
    )

    if not lead:

        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return LeadDetailResponse(
        id=lead.id,
        title=lead.title,
        company=lead.company,
        status=lead.status,
        estimated_value=float(
            lead.estimated_value or 0
        ),
        probability=lead.probability or 0,
        source=lead.source,
        assigned_rep=lead.assigned_rep,
        city=lead.city,
        email=lead.email
    )


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=LeadDetailResponse
)
async def create_lead(
    data: LeadCreate,
    db: AsyncSession = Depends(get_db)
):

    lead = Lead(

        id=uuid4(),

        title=data.title.strip(),

        company=data.company.strip(),

        status="NEW",

        estimated_value=
            data.estimated_value or 0,

        probability=
            data.probability or 0,

        source=data.source,

        assigned_rep=data.assigned_rep,

        city=data.city,

        email=data.email
    )

    db.add(lead)

    await db.commit()

    await db.refresh(lead)

    return LeadDetailResponse(
        id=lead.id,
        title=lead.title,
        company=lead.company,
        status=lead.status,
        estimated_value=float(
            lead.estimated_value or 0
        ),
        probability=lead.probability or 0,
        source=lead.source,
        assigned_rep=lead.assigned_rep,
        city=lead.city,
        email=lead.email
    )


# =========================================================
# PATCH
# =========================================================

@router.patch(
    "/{lead_id}",
    response_model=LeadDetailResponse
)
async def update_lead(
    lead_id: str,
    data: LeadUpdate,
    db: AsyncSession = Depends(get_db)
):

    lead = await db.get(
        Lead,
        lead_id
    )

    if not lead:

        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    payload = data.model_dump(
        exclude_unset=True
    )

    for key, value in payload.items():

        setattr(
            lead,
            key,
            value
        )

    await db.commit()

    await db.refresh(lead)

    return LeadDetailResponse(
        id=lead.id,
        title=lead.title,
        company=lead.company,
        status=lead.status,
        estimated_value=float(
            lead.estimated_value or 0
        ),
        probability=lead.probability or 0,
        source=lead.source,
        assigned_rep=lead.assigned_rep,
        city=lead.city,
        email=lead.email
    )


# =========================================================
# DELETE
# =========================================================

@router.delete(
    "/{lead_id}"
)
async def delete_lead(
    lead_id: str,
    db: AsyncSession = Depends(get_db)
):

    lead = await db.get(
        Lead,
        lead_id
    )

    if not lead:

        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    await db.delete(lead)

    await db.commit()

    return {
        "deleted": True
    }


# =========================================================
# CONVERT TO OPPORTUNITY
# =========================================================

@router.post(
    "/{lead_id}/convert"
)
async def convert_lead(
    lead_id: str,
    db: AsyncSession = Depends(get_db)
):

    lead = await db.get(
        Lead,
        lead_id
    )

    if not lead:

        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    opportunity = Opportunity(

        id=uuid4(),

        title=lead.title,

        customer_id=None,

        stage="QUALIFIED",

        estimated_value=
            lead.estimated_value or 0,

        probability=
            lead.probability or 10,

        close_date=None
    )

    db.add(opportunity)

    lead.status = "CONVERTED"

    await db.commit()

    await db.refresh(opportunity)

    return {
        "opportunity_id":
            str(opportunity.id)
    }