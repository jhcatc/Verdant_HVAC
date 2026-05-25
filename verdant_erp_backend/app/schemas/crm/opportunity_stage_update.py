from pydantic import BaseModel


class OpportunityStageUpdate(BaseModel):

    stage: str