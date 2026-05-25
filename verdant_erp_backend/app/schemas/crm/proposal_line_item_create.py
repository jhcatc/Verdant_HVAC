from pydantic import BaseModel


class ProposalLineItemCreate(BaseModel):
    item_type: str
    description: str = ""
    qty: float = 1
    unit_price: float = 0
    unit_cost: float = 0
    tax_percent: float = 0
    discount_percent: float = 0
    is_optional: bool = False