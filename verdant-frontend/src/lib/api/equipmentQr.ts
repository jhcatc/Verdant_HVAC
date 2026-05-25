import { api } from './client';

export async function getEquipmentQr(
    equipmentId: string
) {

    const response = await api.get(
        `/equipment/${equipmentId}/qr`
    );

    return response.data;
}