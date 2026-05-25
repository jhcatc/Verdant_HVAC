import { runHeartbeatMonitor } from '../jobs/heartbeat-monitor';

let started = false;

export function startHeartbeatMonitor() {
    if (started) return;

    started = true;

    console.log('[Heartbeat Monitor] started');

    setInterval(async () => {
        try {
            await runHeartbeatMonitor();
        } catch (err) {
            console.error('[Heartbeat Monitor] error:', err);
        }
    }, 60_000);
}

let running = false;

setInterval(async () => {
    if (running) return;

    running = true;

    try {
        await runHeartbeatMonitor();
    } finally {
        running = false;
    }
}, 60_000);