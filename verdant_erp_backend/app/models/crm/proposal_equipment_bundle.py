from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Float, ForeignKey, String
from app.core.database import Base

class ProposalEquipmentBundle(Base):

    __tablename__ = "proposal_equipment_bundles"

    id = Column(String, primary_key=True)
    proposal_id = Column(
        UUID(as_uuid=True),
        ForeignKey("crm_proposals.id"),
    )
    name = Column(String)
    description = Column(String)
    total = Column(Float)