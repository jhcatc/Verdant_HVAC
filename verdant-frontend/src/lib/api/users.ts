import api from './client';

export async function getTechnicians() {
    const res = await api.get('/users/technicians');
    return res.data;
}