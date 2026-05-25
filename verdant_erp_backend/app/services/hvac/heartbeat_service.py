from datetime import datetime, timedelta

ONLINE_THRESHOLD_MINUTES = 5


async def update_heartbeat(db, equipment_id: str):
    await db.execute(
        """
        UPDATE equipment
        SET last_heartbeat = $1,
            status = 'online'
        WHERE id = $2
        """,
        [datetime.utcnow(), equipment_id]
    )


async def mark_offline_equipment(db):
    threshold = datetime.utcnow() - timedelta(minutes=ONLINE_THRESHOLD_MINUTES)

    await db.execute(
        """
        UPDATE equipment
        SET status = 'offline'
        WHERE last_heartbeat IS NULL
           OR last_heartbeat < $1
        """,
        [threshold]
    )