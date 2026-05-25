import { json } from '@sveltejs/kit';
import { updateHeartbeat } from '$lib/server/heartbeat';
import { db } from '$lib/server/db';

export async function POST({ request }) {
    const { equipmentId } = await request.json();

    await updateHeartbeat(db, equipmentId);

    return json({ ok: true });
}