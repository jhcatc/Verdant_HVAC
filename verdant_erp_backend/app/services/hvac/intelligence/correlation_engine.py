from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hvac.equipment import Equipment
from app.models.service_order import ServiceOrder
from app.models.service_order_assignment import ServiceOrderAssignment
from app.models.user import User


# =========================================================
# 1. CUSTOMER FAILURE CLUSTERS
# =========================================================

async def customer_failure_clusters(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.customer_id,
            func.count(ServiceOrder.id).label("total_failures")
        )
        .join(ServiceOrder, ServiceOrder.equipment_id == Equipment.id)
        .group_by(Equipment.customer_id)
        .order_by(func.count(ServiceOrder.id).desc())
    )

    rows = result.all()

    if not rows:
        return []

    avg = sum(r.total_failures for r in rows) / len(rows)

    return [
        {
            "customer_id": r.customer_id,
            "total_failures": r.total_failures,
            "risk_level": (
                "critical" if r.total_failures > avg * 1.5
                else "medium" if r.total_failures > avg
                else "low"
            )
        }
        for r in rows
    ]


# =========================================================
# 2. PROBLEMATIC EQUIPMENT RANKING
# =========================================================

async def problematic_equipment(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.id,
            Equipment.asset_tag,
            Equipment.customer_id,
            func.count(ServiceOrder.id).label("failures")
        )
        .join(ServiceOrder, ServiceOrder.equipment_id == Equipment.id)
        .group_by(Equipment.id, Equipment.asset_tag, Equipment.customer_id)
        .order_by(func.count(ServiceOrder.id).desc())
    )

    return [
        {
            "equipment_id": r.id,
            "asset_tag": r.asset_tag,
            "customer_id": r.customer_id,
            "failures": r.failures
        }
        for r in result.all()
    ]


# =========================================================
# 3. INSTALLATION RANKING (FACILITY HEALTH)
# =========================================================

async def installation_ranking(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.location_id,
            func.count(ServiceOrder.id).label("failures")
        )
        .join(ServiceOrder, ServiceOrder.equipment_id == Equipment.id)
        .group_by(Equipment.location_id)
        .order_by(func.count(ServiceOrder.id).desc())
    )

    rows = result.all()

    if not rows:
        return []

    return [
        {
            "location_id": r.location_id,
            "failures": r.failures,
            "risk": (
                "high" if r.failures > 10
                else "medium" if r.failures > 5
                else "low"
            )
        }
        for r in rows
    ]


# =========================================================
# 4. TECHNICIAN HEATMAP (LOAD + ACTIVITY)
# =========================================================

async def technician_heatmap(db: AsyncSession):

    result = await db.execute(
        select(
            User.id,
            User.name,
            func.count(ServiceOrderAssignment.id).label("assignments")
        )
        .join(ServiceOrderAssignment, ServiceOrderAssignment.user_id == User.id)
        .group_by(User.id, User.name)
        .order_by(func.count(ServiceOrderAssignment.id).desc())
    )

    rows = result.all()

    if not rows:
        return []

    return [
        {
            "technician_id": r.id,
            "name": r.name,
            "workload": r.assignments,
            "load_level": (
                "high" if r.assignments > 20
                else "medium" if r.assignments > 10
                else "low"
            )
        }
        for r in rows
    ]


# =========================================================
# 5. MASTER SNAPSHOT (CORRELATION ENGINE ENTRY POINT)
# =========================================================

async def build_correlation_snapshot(db: AsyncSession):

    return {
        "customer_clusters": await customer_failure_clusters(db),
        "problematic_equipment": await problematic_equipment(db),
        "installation_ranking": await installation_ranking(db),
        "technician_heatmap": await technician_heatmap(db)
    }