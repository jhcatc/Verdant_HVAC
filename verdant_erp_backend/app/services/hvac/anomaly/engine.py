from sqlalchemy import text
from datetime import datetime
import uuid

from app.services.hvac.anomaly.rules import (
    detect_temperature_anomaly,
    detect_energy_spike,
    detect_pressure_instability
)


async def detect_anomalies(db):
    """
    Manual anomaly detection engine.
    NO automation, NO dispatch, NO service orders.
    Only internal tickets.
    """

    result = await db.execute(text("""
        SELECT
            equipment_id,
            temperature,
            pressure,
            energy_kw,
            created_at
        FROM equipment_telemetry
        WHERE created_at >= NOW() - INTERVAL '24 hours'
        ORDER BY equipment_id, created_at DESC
    """))

    rows = result.fetchall()

    grouped = {}

    for r in rows:
        grouped.setdefault(r.equipment_id, []).append(r)

    tickets_created = []

    for equipment_id, records in grouped.items():

        anomalies = []

        anomalies += detect_temperature_anomaly(records)
        anomalies += detect_energy_spike(records)
        anomalies += detect_pressure_instability(records)

        for a in anomalies:

            ticket_id = str(uuid.uuid4())

            await db.execute(text("""
                INSERT INTO anomaly_tickets (
                    id,
                    equipment_id,
                    type,
                    severity,
                    title,
                    description,
                    metric_snapshot
                )
                VALUES (
                    :id,
                    :equipment_id,
                    :type,
                    :severity,
                    :title,
                    :description,
                    :snapshot
                )
            """), {
                "id": ticket_id,
                "equipment_id": equipment_id,
                "type": a["type"],
                "severity": a["severity"],
                "title": a["title"],
                "description": a["description"],
                "snapshot": str(a["snapshot"])
            })

            tickets_created.append({
                "id": ticket_id,
                "equipment_id": equipment_id,
                **a
            })

    await db.commit()

    return tickets_created