export type AnomalyType =
    | 'EFFICIENCY_DROP'
    | 'COMPRESSOR_RISK'
    | 'TECHNICIAN_DEVIATION'
    | 'EQUIPMENT_RECURRENCE';

export interface Anomaly {
    id: string;
    type: AnomalyType;

    equipment_id?: string;
    technician_id?: string;
    service_order_id?: string;

    severity: 'low' | 'medium' | 'high';

    score: number; // 0 - 100

    description: string;

    created_at: Date;
}