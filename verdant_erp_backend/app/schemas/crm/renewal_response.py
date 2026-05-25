from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class RenewalResponse(BaseModel):

    contract_id: str
    customer_id: str
    customer_name: str
    renewal_date: datetime | None = None
    sla_tier: str | None = None
    total_value: Decimal | None = None
    status: str | None = None

    class Config:
        from_attributes = True