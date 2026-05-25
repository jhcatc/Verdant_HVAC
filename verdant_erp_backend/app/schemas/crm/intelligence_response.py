from pydantic import BaseModel


class CRMIntelligenceResponse(BaseModel):
    open_pipeline_value: float
    active_contracts: int
    renewals_due: int
    avg_win_probability: float
    high_risk_opportunities: int
    total_customers: int