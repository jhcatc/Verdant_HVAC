from app.models.crm.contract import Contract
from sqlalchemy.ext.asyncio import AsyncSession


class ContractsService:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, contract: Contract):
        self.db.add(contract)
        await self.db.commit()
        await self.db.refresh(contract)
        return contract

    async def get_by_id(self, contract_id: str):
        return await self.db.get(Contract, contract_id)