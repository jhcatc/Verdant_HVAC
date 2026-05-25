from app.models.crm.proposal_line_item import (
    ProposalLineItem
)


def calculate_line_item_total(
    item: ProposalLineItem
):

    subtotal = (
        item.qty
        * item.unit_price
    )

    discount = (
        subtotal
        * (item.discount_percent / 100)
    )

    taxable = subtotal - discount

    tax = (
        taxable
        * (item.tax_percent / 100)
    )

    total = taxable + tax

    return round(total, 2)


def calculate_proposal_totals(
    items: list[ProposalLineItem]
):

    subtotal = 0
    discounts = 0
    taxes = 0
    total = 0
    cost = 0

    for item in items:

        item_subtotal = (
            item.qty
            * item.unit_price
        )

        item_discount = (
            item_subtotal
            * (
                item.discount_percent
                / 100
            )
        )

        taxable = (
            item_subtotal
            - item_discount
        )

        item_tax = (
            taxable
            * (
                item.tax_percent
                / 100
            )
        )

        item_total = taxable + item_tax

        subtotal += item_subtotal
        discounts += item_discount
        taxes += item_tax
        total += item_total

    return {
        "subtotal": round(subtotal, 2),
        "discounts": round(discounts, 2),
        "taxes": round(taxes, 2),
        "grand_total": round(total, 2)
    }