from sqlalchemy import text


async def compute_risk_scores(db):

    result = await db.execute(text("""
        SELECT
            e.id,
            e.asset_tag,
            COUNT(so.id) AS failures,
            COUNT(at.id) AS anomalies
        FROM equipment e
        LEFT JOIN service_orders so ON so.equipment_id = e.id
        LEFT JOIN anomaly_tickets at ON at.equipment_id = e.id
        GROUP BY e.id, e.asset_tag
    """))

    rows = result.fetchall()

    output = []

    for r in rows:

        score = (r.failures * 2) + (r.anomalies * 1)

        if score < 5:
            level = "green"
        elif score < 15:
            level = "yellow"
        else:
            level = "red"

        output.append({
            "equipment_id": r.id,
            "asset_tag": r.asset_tag,
            "score": score,
            "level": level
        })

    return sorted(output, key=lambda x: x["score"], reverse=True)