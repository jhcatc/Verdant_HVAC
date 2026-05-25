from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.crm.proposal import Proposal


async def generate_proposal_number(
    db: AsyncSession
) -> str:
    year = datetime.utcnow().year
    result = await db.execute(
        select(
            func.count(Proposal.id)
        )
    )
    count = result.scalar() or 0
    next_number = count + 1
    return f"PR-{year}-{next_number:06d}"