export type ComponentRegistryItem = {

    id: string;
    equipment_id: string;
    component_type: string;
    component_name: string;
    manufacturer?: string;
    model_number?: string;
    serial_number?: string;
    status: string;
    installation_date?: string;
    replacement_date?: string;
    warranty_expiration?: string;
    useful_life_months?: string;
    failure_reason?: string;
    replacement_reason?: string;
    notes?: string;
    is_critical: boolean;
    maintenance_log_id?: string;
    created_at: string;
    equipment_asset_tag?: string;
    equipment_model?: string;
    health_score: number;
    warranty_status: string;
    mtbf_days?: number;
    failure_events: number;
};

export type ComponentRegistrySnapshot = {

    total_components: number;
    critical_components: number;
    failed_components: number;
    warranty_expiring: number;
    average_health_score: number;
    items: ComponentRegistryItem[];
};