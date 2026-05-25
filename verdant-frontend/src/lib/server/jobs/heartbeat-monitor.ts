import { markOfflineEquipment } from '../heartbeat';
import { db } from '../db';

export async function runHeartbeatMonitor() {
    await markOfflineEquipment(db);
}