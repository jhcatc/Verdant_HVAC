from sqlalchemy import Column, Integer, String
from app.core.database import Base


class InstallationType(Base):

    __tablename__ = "installation_types"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)