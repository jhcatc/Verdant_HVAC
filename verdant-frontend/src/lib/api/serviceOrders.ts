import { api } from './client';

export async function getServiceOrders() {
    return api.get('/service-orders/');
}

export async function getServiceOrder(id: string) {
    return api.get(`/service-orders/${id}`);
}

export type CreateServiceOrderDto = {
    customer_id: string;
    equipment_id?: string;
    priority: string;
    issue_description: string;
    scheduled_date?: string;
};

export type DispatchServiceOrderDto = {
    technician_id: string;
    scheduled_at?: string;
    notes?: string;
};

export async function suggestDispatch(id: string) {
    return api.get(`/service-orders/${id}/suggest`);
}

export async function getAIDispatch(id: string) {
    return api.get(`/service-orders/${id}/ai-dispatch`);
}

export async function completeServiceOrder(id: string) {
    return api.post(`/service-orders/${id}/complete`);
}

export async function getOptimizedRoutes() {
    return api.get('/service-orders/routing/routes');
}

export async function getRouteHeatmap() {
    return api.get('/service-orders/routing/heatmap');
}

