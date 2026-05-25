export type EquipmentTelemetry = {
    equipment_id: string;
    temperature?: number;
    pressure?: number;
    energy_kw?: number;
    created_at: string;
};

export type ServiceOrderSnapshot = {
    id: string;
    equipment_id: string;
    status: string;
    labor_cost: number;
    materials_cost: number;
    created_at: string;
};

export type AnomalyResult = {
    equipment_id: string;
    type: "EFFICIENCY_DROP" | "OVERHEATING" | "HIGH_CONSUMPTION" | "FAILURE_RISK";
    score: number;
    severity: "LOW" | "MEDIUM" | "HIGH";
    explanation: string;
};

/* ---------------------------------------------------
   1. EFFICIENCY DROP DETECTION
--------------------------------------------------- */

export function detectEfficiencyDrop(
    telemetry: EquipmentTelemetry[]
): AnomalyResult[] {

    if (telemetry.length < 5) return [];

    const results: AnomalyResult[] = [];

    for (let i = 1; i < telemetry.length; i++) {

        const prev = telemetry[i - 1];
        const curr = telemetry[i];

        if (!prev.energy_kw || !curr.energy_kw) continue;

        const drop = (prev.energy_kw - curr.energy_kw) / prev.energy_kw;

        if (drop > 0.25) {
            results.push({
                equipment_id: curr.equipment_id,
                type: "EFFICIENCY_DROP",
                score: drop,
                severity: drop > 0.5 ? "HIGH" : "MEDIUM",
                explanation: `Energy efficiency dropped ${(drop * 100).toFixed(1)}%`
            });
        }
    }

    return results;
}

/* ---------------------------------------------------
   2. OVERHEATING DETECTION
--------------------------------------------------- */

export function detectOverheating(
    telemetry: EquipmentTelemetry[]
): AnomalyResult[] {

    const results: AnomalyResult[] = [];

    for (const t of telemetry) {

        if (!t.temperature) continue;

        if (t.temperature > 85) {
            results.push({
                equipment_id: t.equipment_id,
                type: "OVERHEATING",
                score: t.temperature,
                severity: t.temperature > 95 ? "HIGH" : "MEDIUM",
                explanation: `Temperature reached ${t.temperature}°C`
            });
        }
    }

    return results;
}

/* ---------------------------------------------------
   3. FAILURE RISK FROM SERVICE HISTORY
--------------------------------------------------- */

export function detectFailureRisk(
    orders: ServiceOrderSnapshot[]
): AnomalyResult[] {

    const results: AnomalyResult[] = [];

    const equipmentMap: Record<string, number> = {};

    for (const o of orders) {
        if (o.status === "completed") continue;

        equipmentMap[o.equipment_id] =
            (equipmentMap[o.equipment_id] || 0) + 1;
    }

    for (const [equipment_id, count] of Object.entries(equipmentMap)) {

        if (count >= 3) {
            results.push({
                equipment_id,
                type: "FAILURE_RISK",
                score: count,
                severity: count >= 5 ? "HIGH" : "MEDIUM",
                explanation: `Repeated unresolved service orders: ${count}`
            });
        }
    }

    return results;
}

/* ---------------------------------------------------
   4. MASTER ENGINE
--------------------------------------------------- */

export function runAnomalyEngine(
    telemetry: EquipmentTelemetry[],
    orders: ServiceOrderSnapshot[]
): AnomalyResult[] {

    return [
        ...detectEfficiencyDrop(telemetry),
        ...detectOverheating(telemetry),
        ...detectFailureRisk(orders)
    ];
}