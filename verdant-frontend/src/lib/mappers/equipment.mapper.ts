import type {
    Equipment,
} from '$lib/types/equipment';
import type {
    EquipmentCreatePayload
} from '$lib/api/equipment';


export function mapEquipmentToCreatePayload(
    equipment: Partial<Equipment>
): Partial<EquipmentCreatePayload> {

    return {
        asset_tag:
            equipment.asset_tag ?? '',
        model:
            equipment.model,
        serial_number:
            equipment.serial_number,
        manufacture_year:
            equipment.manufacture_year,
        installation_date:
            equipment.installation_date,
        warranty_expiration:
            equipment.warranty_expiration,
        capacity:
            equipment.capacity,
        seer_rating:
            equipment.seer_rating,
        eer_rating:
            equipment.eer_rating,
        customer_id:
            equipment.customer?.id,
        location_id:
            equipment.location?.id,
        equipment_category_id:
            equipment.category?.id,
        equipment_type_id:
            equipment.equipment_type?.id,
        brand_id:
            equipment.brand?.id,
        equipment_status_id:
            equipment.status?.id,
        refrigerant_type_id:
            equipment.refrigerant?.id,
        voltage_type_id:
            equipment.voltage?.id
    };
}