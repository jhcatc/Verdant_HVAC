from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hvac.equipment import Equipment
from app.models.hvac.pm_schedule import PMSchedule

from app.services.service_order_service import create_service_order


# =========================================================
# CORE PM ENGINE
# =========================================================

async def generate_pm_work_orders(db: AsyncSession):
    """
    HVAC PM ENGINE CORE

    Responsibilities:
    - Find due/overdue PM schedules
    - Auto-generate Service Orders
    - Assign priority
    - Update last_generated_at
    - Calculate next_due_date
    """

    now = datetime.utcnow()

    # =====================================================
    # 1. Get all active PM schedules
    # =====================================================
    query = select(PMSchedule).where(
        PMSchedule.is_active == True
    )

    result = await db.execute(query)
    schedules = result.scalars().all()

    created_orders = []

    # =====================================================
    # 2. Process each schedule
    # =====================================================
    for schedule in schedules:

        equipment: Equipment = schedule.equipment

        if not equipment:
            continue

        # =================================================
        # Check if due
        # =================================================
        last_generated = schedule.last_generated_at
        interval_days = schedule.maintenance_interval_days

        if last_generated:
            next_due = last_generated + timedelta(days=interval_days)
        else:
            next_due = schedule.start_date or now

        # Skip if not due
        if next_due > now:
            continue

        # =================================================
        # 3. Create Service Order (EXISTING MODULE)
        # =================================================
        order = await create_service_order(
            db=db,
            payload={
                "equipment_id": str(equipment.id),
                "customer_id": str(equipment.customer_id),
                "location_id": str(equipment.location_id),
                "title": f"PM Maintenance - {equipment.asset_tag}",
                "priority": "HIGH" if schedule.is_critical else "NORMAL",
                "source": "PM_ENGINE",
                "scheduled_date": now.date(),
                "description": schedule.description or "Preventive Maintenance Auto-Generated"
            }
        )

        created_orders.append(order)

        # =================================================
        # 4. Update schedule tracking
        # =================================================
        schedule.last_generated_at = now
        schedule.next_due_date = now + timedelta(days=interval_days)

        db.add(schedule)

    # =====================================================
    # 5. Commit all changes
    # =====================================================
    await db.commit()

    return {
        "generated_orders": len(created_orders),
        "orders": created_orders
    }


# =========================================================
# OVERDUE CHECK ENGINE
# =========================================================

async def get_overdue_pm_schedules(db: AsyncSession):
    """
    Returns schedules that are past due date
    """

    now = datetime.utcnow()

    query = select(PMSchedule).where(
        PMSchedule.next_due_date < now,
        PMSchedule.is_active == True
    )

    result = await db.execute(query)
    return result.scalars().all()