from pydantic import BaseModel
from typing import List

from app.schemas.crm.customer_summary_response import (
    CustomerSummaryResponse
)
from app.schemas.crm.contract_response import (
    ContractResponse
)
from app.schemas.crm.opportunity_response import (
    OpportunityResponse
)

class Customer360Response(BaseModel):
    customer: CustomerSummaryResponse
    contracts: List[ContractResponse]
    opportunities: List[OpportunityResponse]
    renewals: list = []
    facilities: list = []
    service_history: list = []