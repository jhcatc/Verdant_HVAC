import { api } from './client';

export async function getComponents(
    equipmentId: string
) {

    const response = await api.get(
        `/equipment/${equipmentId}/components`
    );

    return response.data;
}

import type {
    EquipmentComponent
} from '$lib/types/components';

export type CreateComponentDto =
Omit<EquipmentComponent, 'id'>;

export async function createComponent(
    equipmentId: string,
    payload: CreateComponentDto
)