import uuid
from datetime import datetime
from sqlalchemy import text
from app.core.ws_manager import manager
from app.core.redis import redis_client


async def ingest_telemetry(db, data: dict):

    equipment_id = data["equipment_id"]

    # =====================================================
    # 1. INSERT TELEMETRY (RAW SQL - tu estilo actual)
    # =====================================================

    await db.execute(
        text("""
            INSERT INTO equipment_telemetry (
                id,
                equipment_id,
                temperature,
                pressure,
                energy_kw,
                created_at
            )
            VALUES (
                :id,
                :equipment_id,
                :temperature,
                :pressure,
                :energy_kw,
                :created_at
            )
        """),
        {
            "id": uuid.uuid4(),
            "equipment_id": equipment_id,
            "temperature": data.get("temperature"),
            "pressure": data.get("pressure"),
            "energy_kw": data.get("energy_kw"),
            "created_at": datetime.utcnow()
        }
    )

    # =====================================================
    # 2. HEARTBEAT UPDATE
    # =====================================================

    await db.execute(
        text("""
            UPDATE equipment
            SET last_heartbeat = :now,
                status = 'online'
            WHERE id = :id
        """),
        {
            "id": equipment_id,
            "now": datetime.utcnow()
        }
    )

    # =====================================================
    # 3. REDIS STREAM
    # =====================================================

    await redis_client.publish(
        "telemetry",
        str(data)
    )

    # =====================================================
    # 4. WEBSOCKET REALTIME
    # =====================================================

    await manager.broadcast({
        "type": "telemetry_update",
        "equipment_id": equipment_id,
        "payload": data
    })