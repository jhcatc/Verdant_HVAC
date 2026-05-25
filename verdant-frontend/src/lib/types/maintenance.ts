export type MaintenanceMeasurement = {
    id?: string;
    type: string;
    value: string;
    unit?: string;
};

export type MaintenanceComponent = {
    id?: string;
    component_name: string;
    status?: string;
    notes?: string;
};

export type MaintenanceLog = {
    id: string;
    maintenance_type: string;
    technician?: string;
    created_at: string;
    notes?: string;
    equipment_condition?: string;
    refrigerant_added?: number;
    measurements?: MaintenanceMeasurement[];
    components?: MaintenanceComponent[];
};