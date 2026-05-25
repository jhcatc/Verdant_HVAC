from datetime import datetime
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service_order import ServiceOrder
from app.models.service_order_assignment import ServiceOrderAssignment
from app.models.user import User
from app.models.hvac.maintenance_log import MaintenanceLog


# =========================================================
# 1. TECHNICIAN PERFORMANCE SCORING
# =========================================================

async def technician_performance_scoring(db: AsyncSession):
    """
    Score técnico basado en:
    - órdenes completadas
    - tiempo promedio de resolución
    - carga total de trabajo
    """

    completed_orders = await db.execute(
        select(
            User.id.label("technician_id"),
            User.name,

            func.count(ServiceOrder.id).label("completed_orders"),

            func.avg(
                func.extract(
                    'epoch',
                    ServiceOrder.updated_at - ServiceOrder.created_at
                )
            ).label("avg_resolution_time_seconds")
        )
        .join(ServiceOrderAssignment, ServiceOrderAssignment.user_id == User.id)
        .join(ServiceOrder, ServiceOrder.id == ServiceOrderAssignment.service_order_id)
        .where(
            ServiceOrder.status == "completed"
        )
        .group_by(User.id)
    )

    return [
        {
            "technician_id": row.technician_id,
            "name": row.name,
            "completed_orders": row.completed_orders,
            "avg_resolution_time_hours": round((row.avg_resolution_time_seconds or 0) / 3600, 2)
        }
        for row in completed_orders.all()
    ]


# =========================================================
# 2. SLA DASHBOARD (REAL PERFORMANCE)
# =========================================================

async def sla_dashboard(db: AsyncSession):
    """
    SLA basado en:
    - tiempo entre scheduled_at y completion
    - cumplimiento vs atraso
    """

    result = await db.execute(
        select(
            func.count(ServiceOrder.id).label("total"),

            func.count(
                case(
                    (ServiceOrder.updated_at <= ServiceOrder.scheduled_at, 1)
                )
            ).label("on_time"),

            func.count(
                case(
                    (ServiceOrder.updated_at > ServiceOrder.scheduled_at, 1)
                )
            ).label("late")
        )
        .where(ServiceOrder.status == "completed")
    )

    row = result.one()

    total = row.total or 0
    on_time = row.on_time or 0
    late = row.late or 0

    return {
        "total_completed_orders": total,
        "on_time": on_time,
        "late": late,
        "sla_percentage": round((on_time / total) * 100, 2) if total else 0
    }


# =========================================================
# 3. CUSTOMER SATISFACTION (PROXY MODEL)
# =========================================================

async def customer_satisfaction_proxy(db: AsyncSession):
    """
    Proxy de satisfacción basado en:
    - re-trabajos (re-open orders)
    - tiempo de resolución
    - cantidad de logs negativos
    """

    result = await db.execute(
        select(
            ServiceOrder.customer_id,

            func.count(ServiceOrder.id).label("total_orders"),

            func.sum(
                case(
                    (ServiceOrder.status == "reopened", 1),
                    else_=0
                )
            ).label("reopened_orders"),

            func.avg(
                func.extract(
                    'epoch',
                    ServiceOrder.updated_at - ServiceOrder.created_at
                )
            ).label("avg_resolution_time")
        )
        .group_by(ServiceOrder.customer_id)
    )

    return [
        {
            "customer_id": row.customer_id,
            "total_orders": row.total_orders,
            "reopened_orders": row.reopened_orders,
            "avg_resolution_hours": round((row.avg_resolution_time or 0) / 3600, 2),
            "satisfaction_score": max(
                0,
                100 - ((row.reopened_orders or 0) * 10)
            )
        }
        for row in result.all()
    ]


# =========================================================
# 4. TIME TO REPAIR ANALYTICS
# =========================================================

async def time_to_repair_analytics(db: AsyncSession):
    """
    Analiza tiempos de reparación por tipo de orden
    """

    result = await db.execute(
        select(
            ServiceOrder.status,
            func.avg(
                func.extract(
                    'epoch',
                    ServiceOrder.updated_at - ServiceOrder.created_at
                )
            ).label("avg_time")
        )
        .where(ServiceOrder.status == "completed")
        .group_by(ServiceOrder.status)
    )

    return [
        {
            "status": row.status,
            "avg_repair_time_hours": round((row.avg_time or 0) / 3600, 2)
        }
        for row in result.all()
    ]


# =========================================================
# 5. FULL SNAPSHOT (ENTRY POINT)
# =========================================================

async def build_service_intelligence_snapshot(db: AsyncSession):
    """
    Snapshot único para frontend
    (NO automatiza nada, solo lectura)
    """

    return {
        "technician_performance": await technician_performance_scoring(db),
        "sla": await sla_dashboard(db),
        "customer_satisfaction": await customer_satisfaction_proxy(db),
        "time_to_repair": await time_to_repair_analytics(db),
        "generated_at": datetime.utcnow().isoformat()
    }