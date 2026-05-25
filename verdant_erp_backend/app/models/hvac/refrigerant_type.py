from sqlalchemy import Column, Integer, String
from app.core.database import Base


class RefrigerantType(Base):

    __tablename__ = "refrigerant_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)