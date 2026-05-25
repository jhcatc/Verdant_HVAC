from uuid import UUID
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.models.crm.contract import Contract
from app.models.customer import Customer

from app.schemas.crm.contract_create import ContractCreate
from app.schemas.crm.contract_response import ContractResponse

router = APIRouter(
    prefix="/crm/contracts",
    tags=["CRM Contracts"]
)


# =========================================================
# LIST
# =========================================================

@router.get(
    "/",
    response_model=list[ContractResponse]
)
async def list_contracts(
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Contract)
        .options(
            selectinload(Contract.customer)
        )
    )

    rows = result.scalars().all()

    return [
        ContractResponse(
            id=c.id,
            customer_id=c.customer_id,
            customer_name=c.customer.name if c.customer else None,
            status=c.status,
            sla_tier=c.sla_tier,
            total_value=float(c.total_value or 0),
            start_date=c.start_date,
            end_date=c.end_date,
            renewal_date=c.renewal_date,
        )
        for c in rows
    ]


# =========================================================
# GET ONE
# =========================================================

@router.get(
    "/{contract_id}",
    response_model=ContractResponse
)
async def get_contract(
    contract_id: UUID,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Contract)
        .options(
            selectinload(Contract.customer)
        )
        .where(
            Contract.id == contract_id
        )
    )

    contract = result.scalar_one_or_none()

    if not contract:

        raise HTTPException(
            status_code=404,
            detail="Contract not found"
        )

    return ContractResponse(
        id=contract.id,
        customer_id=contract.customer_id,
        customer_name=contract.customer.name if contract.customer else None,
        status=contract.status,
        sla_tier=contract.sla_tier,
        total_value=float(contract.total_value or 0),
        start_date=contract.start_date,
        end_date=contract.end_date,
        renewal_date=contract.renewal_date,
    )


# =========================================================
# CREATE
# =========================================================

@router.post(
    "/",
    response_model=ContractResponse
)
async def create_contract(
    data: ContractCreate,
    db: AsyncSession = Depends(get_db)
):

    customer = await db.get(
        Customer,
        data.customer_id
    )

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    contract = Contract(
        id=uuid.uuid4(),
        customer_id=data.customer_id,
        status=data.status,
        total_value=data.total_value,
        sla_tier=data.sla_tier,
        start_date=data.start_date,
        end_date=data.end_date,
        renewal_date=data.renewal_date,
    )

    db.add(contract)

    await db.commit()

    result = await db.execute(
        select(Contract)
        .options(
            selectinload(Contract.customer)
        )
        .where(
            Contract.id == contract.id
        )
    )

    created_contract = result.scalar_one()

    return ContractResponse(
        id=created_contract.id,
        customer_id=created_contract.customer_id,
        customer_name=created_contract.customer.name
        if created_contract.customer
        else None,
        status=created_contract.status,
        sla_tier=created_contract.sla_tier,
        total_value=float(created_contract.total_value or 0),
        start_date=created_contract.start_date,
        end_date=created_contract.end_date,
        renewal_date=created_contract.renewal_date,
    )