import uuid
from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.maintenance.maintenance_plan import MaintenancePlan
from app.models.service_order import (
    ServiceOrder,
    WorkOrderSource,
    ServiceOrderStatus,
    ServiceOrderPriority
)
from app.models.service_order_task import ServiceOrderTask
from app.models.service_order_log import ServiceOrderLog


# =========================================================
# NEXT RUN CALCULATOR
# =========================================================

def calculate_next_run(plan: MaintenancePlan):

    base_date = plan.last_generated_at or datetime.utcnow()

    return base_date + timedelta(days=plan.frequency_days)


# =========================================================
# SHOULD GENERATE?
# =========================================================

def should_generate(plan: MaintenancePlan):

    if not plan.is_active:
        return False

    next_run = calculate_next_run(plan)

    return datetime.utcnow() >= next_run


# =========================================================
# GENERATE SERVICE ORDER
# =========================================================

async def generate_pm_work_order(
    db: AsyncSession,
    plan: MaintenancePlan
):

    # ==========================================
    # DUPLICATE PROTECTION
    # ==========================================

    existing = await db.execute(
        select(ServiceOrder).where(
            ServiceOrder.maintenance_plan_id == plan.id,
            ServiceOrder.status.in_([
                ServiceOrderStatus.DRAFT,
                ServiceOrderStatus.PENDING,
                ServiceOrderStatus.READY_FOR_DISPATCH,
                ServiceOrderStatus.ASSIGNED,
                ServiceOrderStatus.IN_PROGRESS
            ])
        )
    )

    existing_order = existing.scalar_one_or_none()

    if existing_order:
        return existing_order

    # ==========================================
    # CREATE WORK ORDER
    # ==========================================

    order = ServiceOrder(

        id=uuid.uuid4(),

        title=f"PM - {plan.name}",

        description=plan.description,

        source=WorkOrderSource.preventive_maintenance,

        status=ServiceOrderStatus.PENDING,

        priority=ServiceOrderPriority.medium,

        customer_id=plan.customer_id,

        customer_location_id=plan.customer_location_id,

        equipment_id=plan.equipment_id,

        maintenance_plan_id=plan.id,

        scheduled_at=datetime.utcnow(),

        created_at=datetime.utcnow()
    )

    db.add(order)

    await db.flush()

    # ==========================================
    # CLONE PM TASKS
    # ==========================================

    for pm_task in plan.tasks:

        task = ServiceOrderTask(

            id=uuid.uuid4(),

            order_id=order.id,

            title=pm_task.title,

            description=pm_task.description,

            is_done=False
        )

        db.add(task)

    # ==========================================
    # LOG
    # ==========================================

    log = ServiceOrderLog(

        id=uuid.uuid4(),

        order_id=order.id,

        action="pm_generated",

        description=f"Generated automatically from PM Plan: {plan.name}",

        created_at=datetime.utcnow()
    )

    db.add(log)

    # ==========================================
    # UPDATE PLAN
    # ==========================================

    plan.last_generated_at = datetime.utcnow()

    await db.commit()

    return order


# =========================================================
# MAIN ENGINE
# =========================================================

async def run_pm_generation_engine(
    db: AsyncSession
):

    result = await db.execute(
        select(MaintenancePlan)
    )

    plans = result.scalars().all()

    generated = []

    for plan in plans:

        try:

            if should_generate(plan):

                order = await generate_pm_work_order(
                    db,
                    plan
                )

                generated.append(order)

        except Exception as e:
            print("PM GENERATOR ERROR")
            print(e)

    return generated