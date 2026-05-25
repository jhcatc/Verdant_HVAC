from math import radians, cos, sin, asin, sqrt
from collections import defaultdict
from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.service_order import ServiceOrder
from app.models.service_order_assignment import ServiceOrderAssignment
from app.models.user import User


# =========================================================
# DISTANCE
# =========================================================

def haversine(lat1, lon1, lat2, lon2):
    """
    KM distance
    """

    if not all([lat1, lon1, lat2, lon2]):
        return 999999

    lon1, lat1, lon2, lat2 = map(
        radians,
        [lon1, lat1, lon2, lat2]
    )

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = (
        sin(dlat / 2) ** 2 +
        cos(lat1) *
        cos(lat2) *
        sin(dlon / 2) ** 2
    )

    c = 2 * asin(sqrt(a))

    return 6371 * c


# =========================================================
# ETA
# =========================================================

def estimate_drive_minutes(distance_km: float):
    """
    crude ETA
    """

    avg_speed_kmh = 35

    return round((distance_km / avg_speed_kmh) * 60)


# =========================================================
# ORDER ROUTES
# =========================================================

async def build_routes(db):

    result = await db.execute(
        select(ServiceOrder)
        .options(
            selectinload(ServiceOrder.assignments)
                .selectinload(ServiceOrderAssignment.user),
            selectinload(ServiceOrder.customer),
            selectinload(ServiceOrder.customer_location),
            selectinload(ServiceOrder.equipment)
        )
        .where(ServiceOrder.is_active == True)
    )

    orders = result.scalars().unique().all()

    grouped = defaultdict(list)

    for order in orders:

        if not order.scheduled_at:
            continue

        if not order.assignments:
            continue

        primary = order.assignments[0]

        grouped[str(primary.user_id)].append(order)

    technician_routes = []

    for tech_id, tech_orders in grouped.items():

        tech_orders.sort(
            key=lambda x: x.scheduled_at or datetime.utcnow()
        )

        stops = []

        total_distance = 0

        previous = None

        for idx, order in enumerate(tech_orders):

            distance = 0
            eta = 0

            if previous:

                distance = haversine(
                    previous.latitude,
                    previous.longitude,
                    order.latitude,
                    order.longitude
                )

                eta = estimate_drive_minutes(distance)

                total_distance += distance

            stops.append({
                "sequence": idx + 1,
                "order_id": str(order.id),
                "title": order.title,
                "status": order.status,
                "scheduled_at": (
                    order.scheduled_at.isoformat()
                    if order.scheduled_at
                    else None
                ),
                "customer": (
                    order.customer.name
                    if order.customer
                    else None
                ),
                "equipment": (
                    order.equipment.name
                    if order.equipment
                    else None
                ),
                "address": order.address,
                "city": order.city,
                "latitude": order.latitude,
                "longitude": order.longitude,
                "distance_from_previous_km": round(distance, 2),
                "eta_minutes": eta
            })

            previous = order

        technician_routes.append({
            "technician_id": tech_id,
            "technician_name": (
                tech_orders[0]
                .assignments[0]
                .user
                .full_name
            ),
            "orders": stops,
            "total_orders": len(stops),
            "total_distance_km": round(total_distance, 2)
        })

    return technician_routes


# =========================================================
# HEATMAP
# =========================================================

async def build_heatmap(db):

    result = await db.execute(
        select(ServiceOrder)
        .where(
            ServiceOrder.latitude.isnot(None),
            ServiceOrder.longitude.isnot(None),
            ServiceOrder.is_active == True
        )
    )

    orders = result.scalars().all()

    return [
        {
            "lat": o.latitude,
            "lng": o.longitude,
            "weight": (
                4 if o.priority == "urgent"
                else 3 if o.priority == "high"
                else 2 if o.priority == "medium"
                else 1
            ),
            "status": o.status
        }
        for o in orders
    ]