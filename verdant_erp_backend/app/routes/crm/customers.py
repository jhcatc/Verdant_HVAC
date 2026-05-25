from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.customer import Customer
from app.models.crm.contract import Contract
from app.models.crm.opportunity import Opportunity
from app.schemas.crm.customer_360_response import (
    Customer360Response
)

router = APIRouter(
    prefix="/crm/customers",
    tags=["CRM Customers"]
)


@router.get(
    "/{customer_id}",
    response_model=Customer360Response
)
async def get_customer_360(
    customer_id: str,
    db: AsyncSession = Depends(get_db)
):

    # =====================================================
    # CUSTOMER
    # =====================================================

    customer_result = await db.execute(
        select(Customer).where(
            Customer.id == customer_id
        )
    )

    customer = customer_result.scalar_one_or_none()

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # =====================================================
    # CONTRACTS
    # =====================================================

    contracts_result = await db.execute(
        select(Contract).where(
            Contract.customer_id == customer.id
        )
    )

    contracts = contracts_result.scalars().all()

    # =====================================================
    # OPPORTUNITIES
    # =====================================================

    opportunities_result = await db.execute(
        select(Opportunity).where(
            Opportunity.customer_id == customer.id
        )
    )

    opportunities = opportunities_result.scalars().all()

    # =====================================================
    # METRICS
    # =====================================================

    total_revenue = sum(
        float(c.total_value or 0)
        for c in contracts
    )

    # =====================================================
    # RESPONSE
    # =====================================================

    return Customer360Response(

        customer={

            "id": str(customer.id),
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "city": customer.city,
            "annual_revenue": total_revenue,
            "active_contracts": len(contracts),
            "open_opportunities": len(opportunities),
        },

        contracts=[

            {
                "id": str(c.id),
                "status": c.status,
                "sla_tier": c.sla_tier,
                "total_value": float(c.total_value or 0),
                "start_date": c.start_date,
                "end_date": c.end_date,
                "renewal_date": c.renewal_date,
            }

            for c in contracts
        ],

        opportunities=[

            {
                "id": str(o.id),
                "title": o.title,
                "stage": o.stage,
                "estimated_value": float(
                    o.estimated_value or 0
                ),
                "probability": o.probability,
                "close_date": o.close_date,
            }

            for o in opportunities
        ],

        # TODO:
        # Replace with real services later

        renewals=[],
        facilities=[],
        service_history=[],
    )