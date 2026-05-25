from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hvac.equipment import Equipment
from app.models.service_order import ServiceOrder


# =========================================================
# 1. GEO FAILURES (BASE PARA MAPA)
# =========================================================

async def geo_failures(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.location_id,
            func.count(ServiceOrder.id).label("failures")
        )
        .join(ServiceOrder, ServiceOrder.equipment_id == Equipment.id)
        .group_by(Equipment.location_id)
    )

    return [
        {
            "location_id": r.location_id,
            "failures": r.failures
        }
        for r in result.all()
    ]


# =========================================================
# 2. FACILITY HEALTH SCORE (UNIFICADO)
# =========================================================

async def facility_health_score(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.location_id,
            func.count(ServiceOrder.id).label("failures")
        )
        .join(ServiceOrder, ServiceOrder.equipment_id == Equipment.id)
        .group_by(Equipment.location_id)
    )

    output = []

    for r in result.all():

        # score simple, extensible luego (SLA + cost + uptime)
        if r.failures == 0:
            score = 100
        elif r.failures < 5:
            score = 80
        elif r.failures < 10:
            score = 60
        else:
            score = 30

        output.append({
            "location_id": r.location_id,
            "health_score": score,
            "failures": r.failures,
            "status": (
                "healthy" if score >= 80
                else "warning" if score >= 50
                else "critical"
            )
        })

    return output


# =========================================================
# 3. FAKE GEO HEATMAP DATA (READY FOR POSTGIS LATER)
# =========================================================

async def geo_heatmap_points(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.location_id,
            func.count(ServiceOrder.id).label("intensity")
        )
        .join(ServiceOrder, ServiceOrder.equipment_id == Equipment.id)
        .group_by(Equipment.location_id)
    )

    return [
        {
            "location_id": r.location_id,
            "intensity": r.intensity,
            # placeholder geo (luego se reemplaza por PostGIS)
            "lat": None,
            "lng": None
        }
        for r in result.all()
    ]


# =========================================================
# 4. CLUSTERING SIMPLIFICADO (NO ML, SOLO GROUPING)
# =========================================================

async def failure_clusters(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.customer_id,
            Equipment.location_id,
            func.count(ServiceOrder.id).label("failures")
        )
        .join(ServiceOrder, ServiceOrder.equipment_id == Equipment.id)
        .group_by(Equipment.customer_id, Equipment.location_id)
    )

    clusters = []

    for r in result.all():

        cluster_size = r.failures

        clusters.append({
            "customer_id": r.customer_id,
            "location_id": r.location_id,
            "cluster_strength": cluster_size,
            "cluster_type": (
                "hotspot" if cluster_size > 10
                else "medium_cluster" if cluster_size > 5
                else "low_cluster"
            )
        })

    return clusters


# =========================================================
# 5. MASTER VISUAL SNAPSHOT (UI READY)
# =========================================================

async def build_visual_intelligence_snapshot(db: AsyncSession):

    return {
        "facility_health": await facility_health_score(db),
        "geo_heatmap": await geo_heatmap_points(db),
        "clusters": await failure_clusters(db),
        "geo_failures": await geo_failures(db)
    }