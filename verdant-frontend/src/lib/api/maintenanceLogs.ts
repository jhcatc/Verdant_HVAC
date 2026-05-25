import axios from 'axios';

export async function getEquipmentLogs(
    equipmentId: string
) {
    const response = await api.get(
        `/maintenance-logs/equipment/${equipmentId}`
    );

    return response.data;
}

export type CreateMaintenancePlanDto = {
    name: string;
    customer_id: string;
    interval: string;
    maintenance_type: string;
    equipment_ids?: string[];
};
payload: CreateMaintenancePlanDto