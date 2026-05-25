from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from datetime import datetime, timedelta
from math import radians, sin, cos, sqrt, atan2

from app.models.user import User
from app.models.role import Role
from app.models.service_order import ServiceOrder
from app.models.service_order_assignment import ServiceOrderAssignment


# =========================================================
# GEO
# =========================================================

def haversine(lat1, lon1, lat2, lon2):

    if not lat1 or not lon1 or not lat2 or not lon2:
        return 999999

    R = 6371

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# =========================================================
# LOAD
# =========================================================

async def technician_workload(
    db: AsyncSession,
    technician_id
):

    today = datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    tomorrow = today + timedelta(days=1)

    result = await db.execute(
        select(ServiceOrder)
        .join(ServiceOrderAssignment)
        .where(
            ServiceOrderAssignment.user_id == technician_id,
            ServiceOrder.scheduled_at >= today,
            ServiceOrder.scheduled_at < tomorrow,
            ServiceOrder.is_active == True
        )
    )

    orders = result.scalars().all()

    total_hours = sum([
        o.duration_hours or 1
        for o in orders
    ])

    return {
        "orders": len(orders),
        "hours": total_hours
    }


# =========================================================
# REGION CLUSTER
# =========================================================

async def technician_region_density(
    db: AsyncSession,
    technician_id,
    city: str | None
):

    if not city:
        return 0

    result = await db.execute(
        select(func.count(ServiceOrder.id))
        .join(ServiceOrderAssignment)
        .where(
            ServiceOrderAssignment.user_id == technician_id,
            ServiceOrder.city == city
        )
    )

    return result.scalar() or 0


# =========================================================
# SCORE ENGINE
# =========================================================

async def suggest_best_technicians(
    db: AsyncSession,
    order_id: str
):

    result = await db.execute(
        select(ServiceOrder)
        .options(
            selectinload(ServiceOrder.assignments)
        )
        .where(ServiceOrder.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        return []

    # =====================================================
    # TECHNICIANS
    # =====================================================

    techs_result = await db.execute(
        select(User)
        .join(Role)
        .where(
            Role.name == "TECHNICIAN",
            User.is_active == True
        )
    )

    technicians = techs_result.scalars().all()

    recommendations = []

    for tech in technicians:

        workload = await technician_workload(
            db,
            tech.id
        )

        regional_density = await technician_region_density(
            db,
            tech.id,
            order.city
        )

        # =================================================
        # LAST ASSIGNED ORDER GEO
        # =================================================

        last_result = await db.execute(
            select(ServiceOrder)
            .join(ServiceOrderAssignment)
            .where(
                ServiceOrderAssignment.user_id == tech.id,
                ServiceOrder.latitude.isnot(None),
                ServiceOrder.longitude.isnot(None)
            )
            .order_by(ServiceOrder.scheduled_at.desc())
            .limit(1)
        )

        last_order = last_result.scalar_one_or_none()

        distance_score = 100

        if last_order and order.latitude and order.longitude:

            km = haversine(
                last_order.latitude,
                last_order.longitude,
                order.latitude,
                order.longitude
            )

            distance_score = max(0, 100 - km)

        # =================================================
        # WORKLOAD SCORE
        # =================================================

        workload_score = max(
            0,
            100 - (workload["hours"] * 10)
        )

        # =================================================
        # REGION SCORE
        # =================================================

        region_score = regional_density * 10

        # =================================================
        # FINAL
        # =================================================

        final_score = (
            distance_score * 0.45
            + workload_score * 0.35
            + region_score * 0.20
        )

        recommendations.append({
            "technician_id": str(tech.id),
            "technician_name": tech.full_name,
            "distance_score": round(distance_score, 2),
            "workload_score": round(workload_score, 2),
            "region_score": round(region_score, 2),
            "workload_hours": workload["hours"],
            "assigned_orders": workload["orders"],
            "final_score": round(final_score, 2)
        })

    recommendations.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return recommendations