from uuid import uuid4
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.crm.proposal import Proposal
from app.models.crm.proposal_version import (
    ProposalVersion
)
from app.models.crm.proposal_line_item import (
    ProposalLineItem
)
from app.services.crm.proposal_calculator import (
    calculate_proposal_totals
)
from app.models.crm.proposal_version import (
    ProposalVersion
)


async def create_proposal_version(
    db: AsyncSession,
    proposal: Proposal
):
    result = await db.execute(
        select(
            func.max(
                ProposalVersion.version_number
            )
        ).where(
            ProposalVersion.proposal_id
            == proposal.id
        )
    )
    current = result.scalar() or 0
    next_version = current + 1
    items = []

    for item in proposal.line_items:
        items.append({
            "id": str(item.id),
            "item_type": item.item_type,
            "description": item.description,
            "qty": item.qty,
            "unit_price": item.unit_price,
            "unit_cost": item.unit_cost,
            "tax_percent": item.tax_percent,
            "discount_percent":
                item.discount_percent,
            "total": item.total
        })
    totals = calculate_proposal_totals(
        proposal.line_items
    )

    snapshot = {

        "proposal": {

            "id": str(proposal.id),

            "proposal_number":
                proposal.proposal_number,

            "title":
                proposal.title,

            "status":
                proposal.status
        },

        "line_items": items,
        "totals": totals
    }

    version = ProposalVersion(
        id=str(uuid4()),
        proposal_id=str(proposal.id),
        version_number=next_version,
        snapshot=snapshot,
        subtotal=totals["subtotal"],
        discounts=totals["discounts"],
        taxes=totals["taxes"],
        total=totals["grand_total"],
        margin=0
    )

    db.add(version)
    await db.commit()
    await db.refresh(version)
    return version


async def create_proposal_snapshot(
    db,
    proposal,
    totals
):

    latest = len(
        proposal.versions
    )

    snapshot = ProposalVersion(
        id=str(uuid4()),
        proposal_id=proposal.id,
        version_number=latest + 1,
        subtotal=totals["subtotal"],
        taxes=totals["taxes"],
        discounts=totals["discounts"],
        total=totals["grand_total"],
        margin=totals.get(
            "margin_total",
            0
        )
    )

    db.add(snapshot)

    return snapshot