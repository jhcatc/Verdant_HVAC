from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.lead import Lead
from app.models.crm.opportunity import Opportunity
from app.models.crm.contract import Contract
from app.schemas.crm.dashboard_response import (
    DashboardResponse,
    DashboardMetricResponse,
    DashboardOpportunityResponse
)

router = APIRouter(
    prefix="/crm/dashboard",
    tags=["CRM Dashboard"]
)


@router.get(
    "/",
    response_model=DashboardResponse
)
async def get_dashboard(
    db: AsyncSession = Depends(get_db)
):

    # =====================================================
    # OPPORTUNITIES
    # =====================================================

    opp_result = await db.execute(

        select(Opportunity).options(
            selectinload(Opportunity.customer)
        )
    )

    opportunities = (
        opp_result.scalars().all()
    )

    pipeline_total = sum(
        float(o.estimated_value or 0)
        for o in opportunities
    )

    # =====================================================
    # RENEWALS
    # =====================================================

    renewals_result = await db.execute(

        select(Contract).options(
            selectinload(Contract.customer)
        )
    )

    renewals = (
        renewals_result.scalars().all()
    )

    # =====================================================
    # LEADS
    # =====================================================

    leads_result = await db.execute(
        select(Lead)
    )

    leads = (
        leads_result.scalars().all()
    )

    qualified = len([

        l for l in leads
        if l.status == "QUALIFIED"

    ])

    conversion_rate = (

        (qualified / len(leads)) * 100
        if leads else 0

    )

    # =====================================================
    # RESPONSE
    # =====================================================

    return DashboardResponse(

        metrics=[

            DashboardMetricResponse(
                title="Open Pipeline",
                value=round(pipeline_total, 2),
                color="text-emerald-400",
                description="Active HVAC sales pipeline"
            ),

            DashboardMetricResponse(
                title="Renewals Due",
                value=len(renewals),
                color="text-cyan-400",
                description="Contracts requiring attention"
            ),

            DashboardMetricResponse(
                title="Qualified Leads",
                value=qualified,
                color="text-yellow-400",
                description="Sales qualified leads"
            ),

            DashboardMetricResponse(
                title="Conversion Rate",
                value=round(conversion_rate, 1),
                color="text-purple-400",
                description="Lead conversion efficiency"
            )
        ],

        opportunities=[

            DashboardOpportunityResponse(
                customer_name=(
                    o.customer.name
                    if o.customer
                    else "Unknown Customer"
                ),

                opportunity_title=o.title,

                estimated_value=float(
                    o.estimated_value or 0
                ),

                stage=o.stage or "UNKNOWN",

                probability=o.probability or 0
            )

            for o in opportunities
        ],

        renewals=[
            
            DashboardRenewalResponse(
                contract_id=str(c.id),
                customer_name=(
                    c.customer.name
                    if c.customer
                    else "Unknown Customer"
                ),
                renewal_date=(
                    c.renewal_date.isoformat()
                    if c.renewal_date
                    else None
                ),
                sla_tier=c.sla_tier,
                total_value=float(c.total_value or 0),
                status=c.status or "ACTIVE"
            )
            for c in renewals
        ],

        field_kpis=DashboardFieldKpisResponse(
            proposal_win_rate=round(conversion_rate, 1),
            average_contract_value=round(
                (
                    sum(float(c.total_value or 0) for c in renewals)
                    / len(renewals)
                ) if renewals else 0,
                2
            ),
            retention_score=91
        )

    )