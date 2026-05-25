from datetime import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.service_order import (
    ServiceOrder,
    ServiceOrderPriority,
    ServiceOrderStatus
)
from app.models.maintenance.maintenance_plan import MaintenancePlan


async def get_sla_dashboard(
    db: AsyncSession
):

    now = datetime.utcnow()

    # =====================================================
    # ORDERS
    # =====================================================

    result = await db.execute(
        select(ServiceOrder)
        .options(
            selectinload(ServiceOrder.assignments),
            selectinload(ServiceOrder.customer),
            selectinload(ServiceOrder.equipment),
            selectinload(ServiceOrder.maintenance_plan)
        )
    )

    orders = result.scalars().all()

    overdue_orders = []

    emergency_orders = []

    completed_orders = 0

    active_orders = 0

    technician_load = {}

    for order in orders:

        if order.status == ServiceOrderStatus.COMPLETED:
            completed_orders += 1

        else:
            active_orders += 1

        # =================================================
        # SLA BREACH
        # =================================================

        if (
            order.scheduled_at
            and order.status != ServiceOrderStatus.COMPLETED
        ):

            if order.scheduled_at < now:

                overdue_orders.append(order)

        # =================================================
        # AUTO ESCALATION
        # =================================================

        if (
            order.priority != ServiceOrderPriority.urgent
            and order.scheduled_at
            and order.status != ServiceOrderStatus.COMPLETED
        ):

            delta = now - order.scheduled_at

            if delta > timedelta(hours=24):

                order.priority = ServiceOrderPriority.urgent

                emergency_orders.append(order)

        # =================================================
        # TECH UTILIZATION
        # =================================================

        for a in order.assignments:

            tech_id = str(a.user_id)

            if tech_id not in technician_load:
                technician_load[tech_id] = {
                    "count": 0
                }

            technician_load[tech_id]["count"] += 1

    # =====================================================
    # PM COMPLIANCE
    # =====================================================

    plans_result = await db.execute(
        select(MaintenancePlan)
    )

    plans = plans_result.scalars().all()

    overdue_pm = []

    compliant_pm = 0

    for plan in plans:

        if not plan.next_run_at:
            continue

        if plan.next_run_at < now:
            overdue_pm.append(plan)

        else:
            compliant_pm += 1

    total_pm = len(plans)

    compliance_score = 0

    if total_pm > 0:

        compliance_score = round(
            (compliant_pm / total_pm) * 100,
            2
        )

    await db.commit()

    return {

        "summary": {

            "total_orders": len(orders),

            "active_orders": active_orders,

            "completed_orders": completed_orders,

            "overdue_orders": len(overdue_orders),

            "emergency_orders": len(emergency_orders),

            "pm_compliance_score": compliance_score,

            "overdue_pm": len(overdue_pm)
        },

        "overdue_orders": overdue_orders,

        "emergency_orders": emergency_orders,

        "overdue_pm_plans": overdue_pm,

        "technician_utilization": technician_load
    }