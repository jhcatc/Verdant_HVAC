from sqlalchemy import text


async def top_problematic_assets(db):

    result = await db.execute(text("""
        SELECT
            e.id,
            e.asset_tag,
            COUNT(so.id) AS total_failures
        FROM equipment e
        LEFT JOIN service_orders so ON so.equipment_id = e.id
        WHERE so.status = 'failed' OR so.status = 'completed'
        GROUP BY e.id, e.asset_tag
        ORDER BY total_failures DESC
        LIMIT 20
    """))

    rows = result.fetchall()

    return [
        {
            "equipment_id": r.id,
            "asset_tag": r.asset_tag,
            "failures": r.total_failures
        }
        for r in rows
    ]
