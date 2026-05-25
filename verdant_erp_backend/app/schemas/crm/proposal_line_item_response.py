from pydantic import BaseModel


class ProposalLineItemResponse(BaseModel):
    id: str
    proposal_id: str
    item_type: str
    description: str | None = None
    qty: float
    unit_price: float
    unit_cost: float
    tax_percent: float
    discount_percent: float
    subtotal: float
    discount_amount: float
    taxable_amount: float
    tax_amount: float
    total: float
    margin_amount: float
    margin_percent: float
    sort_order: int
    is_optional: bool
    class Config:
        from_attributes = True