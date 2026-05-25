from app.models.crm.opportunity import Opportunity
from sqlalchemy.ext.asyncio import AsyncSession


class OpportunitiesService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, opportunity_id: str):
        return await self.db.get(Opportunity, opportunity_id)