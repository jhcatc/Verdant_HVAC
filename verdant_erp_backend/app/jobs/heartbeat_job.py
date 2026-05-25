from app.services.hvac.heartbeat_service import mark_offline_equipment


async def heartbeat_job(db):
    await mark_offline_equipment(db)