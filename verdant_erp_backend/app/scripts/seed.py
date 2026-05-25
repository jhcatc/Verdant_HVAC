import asyncio
from app.core.database import AsyncSessionLocal
from app.models.location import Location
# 🔥 IMPORTAR MODELOS ANTES DE USAR DB
import app.models

from app.core.seed import seed_roles_permissions


async def run():
    async with AsyncSessionLocal() as db:
        await seed_roles_permissions(db)


if __name__ == "__main__":
    asyncio.run(run())

async def seed_locations(db):

    result = await db.execute(sa.select(Location))
    if result.scalars().first():
        return

    db.add_all([
        Location(name="Main Warehouse", code="WH", type="warehouse"),
        Location(name="Van 01", code="V01", type="van"),
        Location(name="Van 02", code="V02", type="van"),
    ])

    await db.commit()