from pydantic import BaseModel
from typing import Optional


class ProposalLineItemUpdate(BaseModel):
    description: Optional[str] = None
    qty: Optional[float] = None
    unit_price: Optional[float] = None
    unit_cost: Optional[float] = None
    tax_percent: Optional[float] = None
    discount_percent: Optional[float] = None
    sort_order: Optional[int] = None
    is_optional: Optional[bool] = None