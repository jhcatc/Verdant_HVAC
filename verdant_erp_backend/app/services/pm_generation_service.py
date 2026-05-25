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


async def generate_pm_work_orders(
    db: AsyncSession
):

    now = datetime.utcnow()

    result = await db.execute(
        select(MaintenancePlan)
    )

    plans = result.scalars().all()

    generated = []

    for plan in plans:

        if not plan.is_active:
            continue

        if not plan.next_run_at:
            continue

        # 🔥 SOLO GENERAR SI YA TOCA
        if plan.next_run_at > now:
            continue

        # 🔥 EVITAR DUPLICADOS
        existing = await db.execute(
            select(ServiceOrder).where(
                ServiceOrder.maintenance_plan_id == plan.id,
                ServiceOrder.scheduled_at >= (
                    now - timedelta(days=1)
                )
            )
        )

        existing_order = existing.scalar_one_or_none()

        if existing_order:
            continue

        order = ServiceOrder(
            id=uuid.uuid4(),

            title=f"PM • {plan.name}",

            description=(
                f"Auto-generated from maintenance plan "
                f"{plan.name}"
            ),

            source=WorkOrderSource.preventive_maintenance,

            status=ServiceOrderStatus.PENDING,

            priority=ServiceOrderPriority.medium,

            customer_id=plan.customer_id,

            customer_location_id=plan.customer_location_id,

            equipment_id=plan.equipment_id,

            maintenance_plan_id=plan.id,

            scheduled_at=plan.next_run_at,

            duration_hours=2,

            created_at=now
        )

        db.add(order)

        await db.flush()

        # ==================================================
        # 🔥 CLONAR TASKS DEL PM
        # ==================================================

        for task in plan.tasks:

            db.add(
                ServiceOrderTask(
                    id=uuid.uuid4(),
                    order_id=order.id,
                    title=task.title,
                    description=task.description
                )
            )

        # ==================================================
        # 🔥 LOG
        # ==================================================

        db.add(
            ServiceOrderLog(
                id=uuid.uuid4(),
                order_id=order.id,
                action="pm_generated",
                description=(
                    f"Generated automatically from PM "
                    f"{plan.name}"
                ),
                created_at=now
            )
        )

        # ==================================================
        # 🔥 NEXT RUN ENGINE
        # ==================================================

        frequency = plan.frequency_days or 30

        plan.last_run_at = now

        plan.next_run_at = (
            now + timedelta(days=frequency)
        )

        generated.append(order)

    await db.commit()

    return {
        "generated": len(generated)
    }