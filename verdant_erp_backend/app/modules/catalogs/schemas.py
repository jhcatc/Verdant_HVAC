from pydantic import BaseModel


class CatalogItemSchema(BaseModel):

    id: int

    name: str

    class Config:

        from_attributes = True


class EquipmentCategorySchema(
    CatalogItemSchema
):

    code: str | None = None


class EquipmentTypeSchema(
    CatalogItemSchema
):

    category_id: int | None = None


class CatalogsResponseSchema(
    BaseModel
):

    equipment_categories: list[
        EquipmentCategorySchema
    ]

    equipment_types: list[
        EquipmentTypeSchema
    ]

    brands: list[
        CatalogItemSchema
    ]
    
    refrigerants: list[
        CatalogItemSchema
    ]

    voltages: list[
        CatalogItemSchema
    ]

    statuses: list[
        CatalogItemSchema
    ]

    installation_types: list[
        CatalogItemSchema
    ]

    power_sources: list[
        CatalogItemSchema
    ]

    maintenance_types: list[
        CatalogItemSchema
    ]