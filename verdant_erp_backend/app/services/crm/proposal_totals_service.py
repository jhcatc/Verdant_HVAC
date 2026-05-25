from app.models.crm.proposal_totals import (
    ProposalTotals
)
from app.services.crm.proposal_calculator import (
    calculate_line_item_total
)

def recalculate_proposal(
    proposal
):

    subtotal = 0
    discount_total = 0
    tax_total = 0
    grand_total = 0
    cost_total = 0
    margin_total = 0
    for item in proposal.line_items:
        calculate_line_item_total(item)
        subtotal += item.subtotal
        discount_total += (
            item.discount_amount
        )
        tax_total += item.tax_amount
        grand_total += item.total
        cost_total += (
            item.qty
            * item.unit_cost
        )
        margin_total += (
            item.margin_amount
        )
    margin_percent = 0
    if grand_total > 0:
        margin_percent = (
            margin_total / grand_total
        ) * 100
    if not proposal.totals:
        proposal.totals = ProposalTotals()
    proposal.totals.subtotal = subtotal
    proposal.totals.discount_total = (
        discount_total
    )
    proposal.totals.tax_total = tax_total
    proposal.totals.grand_total = grand_total
    proposal.totals.cost_total = cost_total
    proposal.totals.margin_total = margin_total
    proposal.totals.margin_percent = (
        margin_percent
    )

    proposal.amount = grand_total