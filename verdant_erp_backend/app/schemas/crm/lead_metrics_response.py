from pydantic import BaseModel


class LeadMetricResponse(BaseModel):
    title: str
    value: str | int | float
    color: str