from sqlalchemy import text


async def equipment_cost_analysis(db):

    result = await db.execute(text("""
        SELECT
            e.id,
            e.asset_tag,
            SUM(so.labor_cost + so.material_cost) AS total_cost,
            COUNT(so.id) AS maintenance_count
        FROM equipment e
        JOIN service_orders so ON so.equipment_id = e.id
        GROUP BY e.id, e.asset_tag
    """))

    rows = result.fetchall()

    return [
        {
            "equipment_id": r.id,
            "asset_tag": r.asset_tag,
            "total_cost": float(r.total_cost or 0),
            "maintenance_count": r.maintenance_count,
            "avg_cost": float(r.total_cost / r.maintenance_count) if r.maintenance_count else 0
        }
        for r in rows
    ]