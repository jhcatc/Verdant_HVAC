import uuid

from datetime import (
    datetime,
    timedelta,
    date
)

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.maintenance.maintenance_plan import (
    MaintenancePlan
)

from app.models.maintenance.maintenance_plan_equipment import (
    MaintenancePlanEquipment
)

from app.models.maintenance.maintenance_task_template import (
    MaintenanceTaskTemplate
)

from app.models.service_order import (
    ServiceOrder,
    ServiceOrderStatus,
    ServiceOrderPriority,
    WorkOrderSource
)

from app.models.service_order_task import (
    ServiceOrderTask
)

from app.models.service_order_log import (
    ServiceOrderLog
)


async def generate_preventive_maintenance_orders(
    db: AsyncSession
):

    today = date.today()

    result = await db.execute(

        select(MaintenancePlan)

        .options(
            selectinload(
                MaintenancePlan.equipment
            ).selectinload(
                MaintenancePlanEquipment.equipment
            ),

            selectinload(
                MaintenancePlan.task_templates
            )
        )

        .where(
            MaintenancePlan.active == True,
            MaintenancePlan.auto_generate_work_orders == True,
            MaintenancePlan.next_run_date <= today
        )
    )

    plans = result.scalars().unique().all()

    generated_orders = []

    for plan in plans:

        if not plan.equipment:
            continue

        for equipment_link in plan.equipment:

            equipment = equipment_link.equipment

            order = ServiceOrder(

                id=uuid.uuid4(),

                title=f"Preventive Maintenance - {equipment.asset_tag}",

                description=plan.description,

                source=WorkOrderSource.preventive_maintenance,

                status=ServiceOrderStatus.READY_FOR_DISPATCH,

                priority=ServiceOrderPriority.medium,

                customer_id=plan.customer_id,

                customer_location_id=plan.location_id,

                equipment_id=equipment.id,

                maintenance_plan_id=plan.id,

                duration_hours=2,

                created_at=datetime.utcnow()
            )

            db.add(order)

            await db.flush()

            """
            CLONE TASK TEMPLATES
            """

            for template in plan.task_templates:

                task = ServiceOrderTask(

                    id=uuid.uuid4(),

                    order_id=order.id,

                    title=template.title,

                    description=template.description
                )

                db.add(task)

            """
            LOG
            """

            db.add(

                ServiceOrderLog(

                    id=uuid.uuid4(),

                    order_id=order.id,

                    action="pm_auto_generated",

                    description=(
                        f"Generated automatically from "
                        f"maintenance plan {plan.name}"
                    ),

                    created_at=datetime.utcnow()
                )
            )

            generated_orders.append(order)

        """
        CALCULATE NEXT RUN
        """

        if plan.frequency_days:

            plan.next_run_date = (
                today +
                timedelta(days=plan.frequency_days)
            )

    await db.commit()

    return {
        "generated": len(generated_orders)
    }