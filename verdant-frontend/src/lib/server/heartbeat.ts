import type { Database } from '$lib/server/db';

export async function updateHeartbeat(db: Database, equipmentId: string) {
    const now = new Date();

    await db.execute(
        `
        UPDATE equipment
        SET last_heartbeat = $1,
            status = 'online'
        WHERE id = $2
        `,
        [now, equipmentId]
    );
}

export async function markOfflineEquipment(db: Database) {
    const threshold = new Date(Date.now() - 5 * 60 * 1000);

    await db.execute(
        `
        UPDATE equipment
        SET status = 'offline'
        WHERE last_heartbeat < $1
           OR last_heartbeat IS NULL
        `,
        [threshold]
    );
}