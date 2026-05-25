import api from './client';

export async function getSLADashboard() {
    return api.get('/sla-engine/dashboard');
}