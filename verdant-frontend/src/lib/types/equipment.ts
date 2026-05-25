import type {
    Brand,
    EquipmentCategory,
    EquipmentStatus,
    EquipmentType,
    RefrigerantType,
    VoltageType
} from './catalogs';

export type Equipment = {

    id: string;
    asset_tag: string;
    model?: string;
    serial_number?: string;
    manufacture_year?: number;
    installation_date?: string;
    warranty_expiration?: string;
    capacity?: string;
    seer_rating?: number;
    eer_rating?: number;
    customer?: {
        id: string;
        name: string;
    };

    location?: {
        id: string;
        name: string;
    };

    category?: EquipmentCategory;
    equipment_type?: EquipmentType;
    brand?: Brand;
    status?: EquipmentStatus;
    refrigerant?: RefrigerantType;
    voltage?: VoltageType;
};