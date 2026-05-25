export type EquipmentComponent = {

    id: string;
    equipment_id: string;
    component_type: string;
    component_name: string;
    manufacturer?: string;
    model_number?: string;
    serial_number?: string;
    install_date?: string;
    warranty_expiration?: string;
    status?: string;
    is_critical?: boolean;
};

export type ComponentMeasurement = {

    id?: string;
    component_id: string;
    measurement_type: string;
    value: number;
    unit?: string;
    recorded_at?: string;
};

export type ComponentFailure = {

    id?: string;
    component_id: string;
    failure_type: string;
    severity?: string;
    notes?: string;
    occurred_at?: string;
};

export type ComponentReplacement = {

    id?: string;
    component_id: string;
    replaced_component_serial?: string;
    replacement_reason?: string;
    replaced_at?: string;
};

    export type Contract = {
        id: string;
        contract_number: string;
        customer: string;
        contract_type: string;
        facility: string;
        sla_level: string;
        annual_value: number;
        renewal_date: string;
        status: string;
    };