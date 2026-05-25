from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalogs import repository


async def get_catalogs(
    db: AsyncSession
):

    return await repository.get_catalogs(
        db
    )