from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.hvac.equipment import Equipment
from app.models.hvac.maintenance_log import MaintenanceLog
from app.services.hvac.intelligence.visual_intelligence_engine import (
    build_visual_intelligence_snapshot
)

# =========================================================
# 1. FAILURES BY CUSTOMER
# =========================================================

async def failures_by_customer(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.customer_id,
            func.count(MaintenanceLog.id).label("failures")
        )
        .join(MaintenanceLog, MaintenanceLog.equipment_id == Equipment.id)
        .group_by(Equipment.customer_id)
    )

    return [
        {
            "customer_id": r.customer_id,
            "failures": r.failures
        }
        for r in result.all()
    ]


# =========================================================
# 2. PROBLEMATIC EQUIPMENT
# =========================================================

async def problematic_equipment(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.id,
            Equipment.asset_tag,
            func.count(MaintenanceLog.id).label("failures")
        )
        .join(MaintenanceLog, MaintenanceLog.equipment_id == Equipment.id)
        .group_by(Equipment.id, Equipment.asset_tag)
        .order_by(func.count(MaintenanceLog.id).desc())
        .limit(20)
    )

    return [
        {
            "equipment_id": r.id,
            "asset_tag": r.asset_tag,
            "failures": r.failures
        }
        for r in result.all()
    ]


# =========================================================
# 3. MAINTENANCE COSTS (BASE MODEL - EXTENSIBLE)
# =========================================================

async def maintenance_costs(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.id,
            Equipment.asset_tag,
            func.count(MaintenanceLog.id).label("repairs")
        )
        .join(MaintenanceLog, MaintenanceLog.equipment_id == Equipment.id)
        .group_by(Equipment.id, Equipment.asset_tag)
    )

    return [
        {
            "equipment_id": r.id,
            "asset_tag": r.asset_tag,
            "estimated_cost": r.repairs * 120  # baseline costo estimado
        }
        for r in result.all()
    ]


# =========================================================
# 4. RISK SCORING (VISUAL ONLY - NO AUTOMATION)
# =========================================================

async def risk_scoring(db: AsyncSession):

    result = await db.execute(
        select(
            Equipment.id,
            Equipment.asset_tag,
            func.count(MaintenanceLog.id).label("failures")
        )
        .join(MaintenanceLog, MaintenanceLog.equipment_id == Equipment.id)
        .group_by(Equipment.id, Equipment.asset_tag)
    )

    output = []

    for r in result.all():

        if r.failures >= 10:
            risk = "CRITICAL"
        elif r.failures >= 5:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        output.append({
            "equipment_id": r.id,
            "asset_tag": r.asset_tag,
            "risk": risk,
            "failures": r.failures
        })

    return output


# =========================================================
# SNAPSHOT (SINGLE UI CALL - CLEAN & COMPLETE)
# =========================================================

async def build_intelligence_snapshot(db: AsyncSession):

    return {
        "failures_by_customer": await failures_by_customer(db),
        "problematic_equipment": await problematic_equipment(db),
        "maintenance_costs": await maintenance_costs(db),
        "risk_scoring": await risk_scoring(db)
    }