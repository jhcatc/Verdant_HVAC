from pydantic import BaseModel


class ProposalStatusUpdate(BaseModel):

    status: str