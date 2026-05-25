from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.crm.contract import Contract
from app.schemas.crm.renewal_response import (
    RenewalResponse
)

router = APIRouter(
    prefix="/crm/renewals",
    tags=["CRM Renewals"]
)


@router.get(
    "/",
    response_model=list[RenewalResponse]
)
async def list_renewals(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Contract)
        .options(
            selectinload(Contract.customer)
        )

        .where(
            Contract.status == "ACTIVE"
        )
    )

    contracts = result.scalars().all()

    return [

        RenewalResponse(
            contract_id=str(c.id),
            customer_id=str(c.customer_id),
            customer_name=(
                c.customer.name
                if c.customer
                else "Unknown Customer"
            ),

            renewal_date=c.renewal_date,
            sla_tier=c.sla_tier,
            total_value=c.total_value,
            status=c.status
        )

        for c in contracts
    ]