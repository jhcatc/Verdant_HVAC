from uuid import uuid4
from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import (
    AsyncSession
)
from sqlalchemy import select
from sqlalchemy.orm import (
    selectinload
)
from app.core.database import get_db
from app.models.crm.proposal import Proposal
from app.models.crm.proposal_line_item import (
    ProposalLineItem
)
from app.schemas.crm.proposal_line_item_create import (
    ProposalLineItemCreate
)
from app.schemas.crm.proposal_line_item_update import (
    ProposalLineItemUpdate
)
from app.services.crm.proposal_totals_service import (
    recalculate_proposal
)
from app.services.crm.proposal_calculator import (
    calculate_line_item_total,
    calculate_proposal_totals
)
from pydantic import BaseModel
from app.schemas.crm.proposal_line_item_response import (
    ProposalLineItemResponse
)

router = APIRouter(
    prefix="/crm/proposals",
    tags=["Proposal Line Items"]
)


class ReorderItem(BaseModel):
    id: str
    sort_order: int


class ReorderPayload(BaseModel):
    items: list[ReorderItem]

@router.post(
    "/{proposal_id}/line-items",
    response_model=ProposalLineItemResponse
)
async def create_line_item(
    proposal_id: str,
    data: ProposalLineItemCreate,
    db: AsyncSession = Depends(get_db)
):
    proposal = await db.execute(
        select(Proposal)
        .options(
            selectinload(
                Proposal.line_items
            ),
            selectinload(
                Proposal.totals
            )
        )
        .where(
            Proposal.id == proposal_id
        )
    )

    proposal = proposal.scalar_one_or_none()

    if not proposal:

        raise HTTPException(
            status_code=404,
            detail="Proposal not found"
        )

    item = ProposalLineItem(
        id=uuid4(),
        proposal_id=proposal_id,
        item_type=data.item_type,
        description=data.description,
        qty=data.qty,
        unit_price=data.unit_price,
        unit_cost=data.unit_cost,
        tax_percent=data.tax_percent,
        discount_percent=(
            data.discount_percent
        ),
        is_optional=data.is_optional,
        sort_order=len(
            proposal.line_items
        )
    )

    proposal.line_items.append(item)
    recalculate_proposal(proposal)
    await db.commit()
    return item


@router.patch(
    "/{proposal_id}/line-items/{item_id}",
    response_model=ProposalLineItemResponse
)
async def update_line_item(
    proposal_id: str,
    item_id: str,
    payload: ProposalLineItemUpdate,
    db: AsyncSession = Depends(get_db)
):

    item = await db.get(
        ProposalLineItem,
        item_id
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Line item not found"
        )

    for key, value in payload.model_dump(
        exclude_unset=True
    ).items():

        setattr(item, key, value)

    item.total = (
        calculate_line_item_total(item)
    )

    await db.commit()
    await db.refresh(item)

    return item

@router.get(
    "/{proposal_id}/line-items",
    response_model=list[
        ProposalLineItemResponse
    ]
)
async def list_line_items(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProposalLineItem)
        .where(
            ProposalLineItem.proposal_id
            == proposal_id
        )
        .order_by(
            ProposalLineItem.sort_order.asc()
        )
    )

    return result.scalars().all()

@router.delete(
    "/{proposal_id}/line-items/{item_id}"
)
async def delete_line_item(
    proposal_id: str,
    item_id: str,
    db: AsyncSession = Depends(get_db)
):
    item = await db.get(
        ProposalLineItem,
        item_id
    )
    if not item:

        raise HTTPException(
            status_code=404,
            detail="Line item not found"
        )

    await db.delete(item)
    await db.commit()

    return {
        "deleted": True
    }

@router.post(
    "/{proposal_id}/line-items/reorder"
)
async def reorder_line_items(
    proposal_id: str,
    payload: ReorderPayload,
    db: AsyncSession = Depends(get_db)
):
    for row in payload.items:

        item = await db.get(
            ProposalLineItem,
            row.id
        )
        if item:
            item.sort_order = (
                row.sort_order
            )

    await db.commit()

    return {
        "success": True
    }

@router.get(
    "/{proposal_id}/totals"
)
async def get_totals(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProposalLineItem)
        .where(
            ProposalLineItem.proposal_id
            == proposal_id
        )
    )
    items = result.scalars().all()

    return calculate_proposal_totals(
        items
    )

@router.post(
    "/{proposal_id}/recalculate"
)
async def recalculate(
    proposal_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProposalLineItem)
        .where(
            ProposalLineItem.proposal_id
            == proposal_id
        )
    )
    items = result.scalars().all()

    for item in items:

        subtotal = (
            item.qty
            * item.unit_price
        )
        discount_amount = (
            subtotal
            * (
                item.discount_percent
                / 100
            )
        )
        taxable = (
            subtotal
            - discount_amount
        )
        tax_amount = (
            taxable
            * (
                item.tax_percent
                / 100
            )
        )
        total = taxable + tax_amount

        cost_total = (
            item.qty
            * item.unit_cost
        )
        margin = total - cost_total

        margin_percent = 0

        if total > 0:

            margin_percent = (
                margin / total
            ) * 100

        item.subtotal = subtotal
        item.discount_amount = discount_amount
        item.taxable_amount = taxable
        item.tax_amount = tax_amount
        item.total = total
        item.margin_amount = margin
        item.margin_percent = margin_percent

    await db.commit()

    return calculate_proposal_totals(
        items
    )