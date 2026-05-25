from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.customer import Customer
from app.models.crm.contract import Contract
from app.models.crm.opportunity import Opportunity
from app.schemas.crm.intelligence_response import (
    CRMIntelligenceResponse
)

router = APIRouter(
    prefix="/crm/intelligence",
    tags=["CRM Intelligence"]
)


@router.get(
    "/",
    response_model=CRMIntelligenceResponse
)
async def crm_intelligence(
    db: AsyncSession = Depends(get_db)
):

    # =====================================================
    # OPEN PIPELINE VALUE
    # =====================================================

    pipeline_result = await db.execute(
        select(
            func.coalesce(
                func.sum(
                    Opportunity.estimated_value
                ),
                0
            )
        ).where(
            Opportunity.stage.not_in([
                "WON",
                "LOST"
            ])
        )
    )

    open_pipeline_value = float(
        pipeline_result.scalar() or 0
    )

    # =====================================================
    # ACTIVE CONTRACTS
    # =====================================================

    active_contracts_result = await db.execute(
        select(
            func.count(Contract.id)
        ).where(
            Contract.status == "ACTIVE"
        )
    )

    active_contracts = (
        active_contracts_result.scalar() or 0
    )

    # =====================================================
    # RENEWALS DUE
    # =====================================================

    next_90_days = datetime.utcnow() + timedelta(days=90)

    renewals_result = await db.execute(
        select(
            func.count(Contract.id)
        ).where(
            Contract.renewal_date.is_not(None),
            Contract.renewal_date <= next_90_days,
            Contract.status == "ACTIVE"
        )
    )

    renewals_due = (
        renewals_result.scalar() or 0
    )

    # =====================================================
    # AVG WIN PROBABILITY
    # =====================================================

    probability_result = await db.execute(
        select(
            func.avg(
                Opportunity.probability
            )
        ).where(
            Opportunity.stage.not_in([
                "WON",
                "LOST"
            ])
        )
    )

    avg_probability = (
        probability_result.scalar() or 0
    )

    # =====================================================
    # HIGH RISK OPPORTUNITIES
    # =====================================================

    high_risk_result = await db.execute(
        select(
            func.count(Opportunity.id)
        ).where(
            Opportunity.probability < 30
        )
    )

    high_risk_opportunities = (
        high_risk_result.scalar() or 0
    )

    # =====================================================
    # TOTAL CUSTOMERS
    # =====================================================

    customers_result = await db.execute(
        select(
            func.count(Customer.id)
        )
    )

    total_customers = (
        customers_result.scalar() or 0
    )

    # =====================================================
    # RESPONSE
    # =====================================================

    return CRMIntelligenceResponse(

        open_pipeline_value=
            round(open_pipeline_value, 2),

        active_contracts=
            active_contracts,

        renewals_due=
            renewals_due,

        avg_win_probability=
            round(float(avg_probability), 2),

        high_risk_opportunities=
            high_risk_opportunities,

        total_customers=
            total_customers
    )