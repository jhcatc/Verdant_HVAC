from datetime import datetime, timedelta
from sqlalchemy import text
import uuid


async def detect_anomalies(db):
    """
    Entrada: historial de equipment_telemetry
    Salida: anomaly tickets (manual review only)
    """

    # 1. traer últimos datos por equipo
    result = await db.execute(text("""
        SELECT *
        FROM equipment_telemetry
        WHERE created_at >= NOW() - INTERVAL '24 hours'
        ORDER BY equipment_id, created_at DESC
    """))

    rows = result.fetchall()

    grouped = {}

    for r in rows:
        grouped.setdefault(r.equipment_id, []).append(r)

    tickets = []

    for equipment_id, data in grouped.items():

        anomalies = []

        anomalies += detect_temperature_anomaly(data)
        anomalies += detect_energy_spike(data)
        anomalies += detect_pressure_instability(data)

        for a in anomalies:

            ticket = {
                "id": str(uuid.uuid4()),
                "equipment_id": equipment_id,
                "type": a["type"],
                "severity": a["severity"],
                "title": a["title"],
                "description": a["description"],
                "metric_snapshot": a["snapshot"],
                "created_at": datetime.utcnow()
            }

            tickets.append(ticket)

            await db.execute(text("""
                INSERT INTO anomaly_tickets
                (id, equipment_id, type, severity, title, description, metric_snapshot)
                VALUES (:id, :equipment_id, :type, :severity, :title, :description, :snapshot)
            """), {
                **ticket,
                "snapshot": str(ticket["metric_snapshot"])
            })

    await db.commit()

    return tickets