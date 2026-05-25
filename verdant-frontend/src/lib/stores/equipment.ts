import { writable }
from 'svelte/store';

import type {
    EquipmentCreatePayload
} from '$lib/api/equipment';

export const equipmentDraft =
    writable<Partial<EquipmentCreatePayload>>({});
