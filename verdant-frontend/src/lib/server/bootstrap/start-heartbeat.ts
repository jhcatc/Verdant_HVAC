import { markOfflineEquipment } from '$lib/api/heartbeat';

let interval: NodeJS.Timeout | null = null;

export function startHeartbeatMonitor() {
    if (interval) return;

    interval = setInterval(async () => {
        try {
            await markOfflineEquipment();
        } catch (err) {
            console.error('[heartbeat]', err);
        }
    }, 60_000);
}