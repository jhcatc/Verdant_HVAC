export async function getVisualIntelligenceSnapshot() {

    const res = await fetch('/api/hvac/visual-intelligence/snapshot');

    if (!res.ok) {
        throw new Error('Failed to load visual intelligence');
    }

    return await res.json();
}