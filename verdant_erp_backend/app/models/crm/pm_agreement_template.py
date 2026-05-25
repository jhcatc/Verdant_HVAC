import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    Integer
)
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class PMAgreementTemplate(Base):
    __tablename__ = "pm_agreement_templates"
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    billing_cycle = Column(String)
    visits_per_year = Column(Integer)
    base_price = Column(Float)