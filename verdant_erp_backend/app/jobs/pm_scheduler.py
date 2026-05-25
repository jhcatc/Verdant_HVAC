from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.database import AsyncSessionLocal
from app.services.hvac.pm_schedule_service import generate_pm_work_orders

import logging

logger = logging.getLogger(__name__)

# =========================================================
# SCHEDULER INSTANCE
# =========================================================

scheduler = AsyncIOScheduler()


# =========================================================
# CORE JOB
# =========================================================

async def run_pm_generation():
    """
    Daily PM Engine Runner
    - Generates preventive maintenance work orders
    - Updates schedules
    - Feeds dispatch system
    """

    async with AsyncSessionLocal() as db:

        try:

            result = await generate_pm_work_orders(db)

            logger.info(
                f"[PM ENGINE] Generated {result['generated_orders']} work orders"
            )

        except Exception as e:

            logger.error(
                f"[PM ENGINE ERROR] {str(e)}"
            )


# =========================================================
# SCHEDULER CONFIGURATION
# =========================================================

def start_pm_scheduler():
    """
    Starts APScheduler job
    Runs daily at 02:00 AM server time
    """

    scheduler.add_job(
        run_pm_generation,
        trigger=CronTrigger(hour=2, minute=0),
        id="pm_daily_generation",
        replace_existing=True,
        max_instances=1,
        coalesce=True
    )

    scheduler.start()

    logger.info("[PM SCHEDULER] Started successfully")


# =========================================================
# STOP FUNCTION (optional lifecycle control)
# =========================================================

def stop_pm_scheduler():

    if scheduler.running:

        scheduler.shutdown()

        logger.info("[PM SCHEDULER] Stopped")