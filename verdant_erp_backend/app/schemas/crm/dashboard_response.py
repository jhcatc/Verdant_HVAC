from pydantic import BaseModel
from typing import List, Optional


class DashboardMetricResponse(BaseModel):
    title: str
    value: float
    color: str
    description: str


class DashboardOpportunityResponse(BaseModel):
    customer_name: str
    opportunity_title: str
    estimated_value: float
    stage: str
    probability: int


class DashboardRenewalResponse(BaseModel):
    contract_id: str
    customer_name: str
    renewal_date: Optional[str] = None
    sla_tier: Optional[str] = None
    total_value: float
    status: str


class DashboardFieldKpisResponse(BaseModel):
    proposal_win_rate: float
    average_contract_value: float
    retention_score: float


class DashboardResponse(BaseModel):
    metrics: List[DashboardMetricResponse]
    opportunities: List[DashboardOpportunityResponse]
    renewals: List[DashboardRenewalResponse]
    field_kpis: DashboardFieldKpisResponse