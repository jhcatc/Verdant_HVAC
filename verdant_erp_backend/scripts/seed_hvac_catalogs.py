import asyncio

from sqlalchemy import select

from app.core.database import (
    AsyncSessionLocal
)

from app.models.hvac import (
    EquipmentCategory,
    EquipmentType,
    Brand,
    RefrigerantType,
    VoltageType,
    PowerSource,
    InstallationType,
    EquipmentStatus,
    MaintenanceType
)


async def seed_if_empty(
    db,
    model,
    items
):

    result = await db.execute(
        select(model)
    )

    exists = result.scalars().first()

    if exists:

        print(
            f'SKIPPED {model.__name__}'
        )

        return

    for item in items:

        db.add(
            model(**item)
        )

    await db.commit()

    print(
        f'SEEDED {model.__name__}'
    )


async def run():

    async with AsyncSessionLocal() as db:

        """
        EQUIPMENT CATEGORIES
        """

        await seed_if_empty(
            db,
            EquipmentCategory,
            [
                {
                    "name": "Air Conditioning"
                },
                {
                    "name": "Heating"
                },
                {
                    "name": "Ventilation"
                },
                {
                    "name": "Hot Water"
                },
                {
                    "name":
                        "Commercial Refrigeration"
                }
            ]
        )

        """
        BRANDS
        """

        await seed_if_empty(
            db,
            Brand,
            [
                {"name": "Carrier"},
                {"name": "Trane"},
                {"name": "Daikin"},
                {"name": "Mitsubishi"},
                {"name": "LG"},
                {"name": "Samsung"},
                {"name": "York"},
                {"name": "Rheem"},
                {"name": "Goodman"}
            ]
        )

        """
        REFRIGERANTS
        """

        await seed_if_empty(
            db,
            RefrigerantType,
            [
                {"name": "R22"},
                {"name": "R410A"},
                {"name": "R32"},
                {"name": "R134A"},
                {"name": "R404A"},
                {"name": "R454B"}
            ]
        )

        """
        VOLTAGES
        """

        await seed_if_empty(
            db,
            VoltageType,
            [
                {"name": "110V"},
                {"name": "220V"},
                {"name": "440V"}
            ]
        )

        """
        POWER SOURCES
        """

        await seed_if_empty(
            db,
            PowerSource,
            [
                {"name": "Electric"},
                {"name": "Natural Gas"},
                {"name": "Diesel"}
            ]
        )

        """
        INSTALLATION TYPES
        """

        await seed_if_empty(
            db,
            InstallationType,
            [
                {"name": "Residential"},
                {"name": "Commercial"},
                {"name": "Industrial"}
            ]
        )

        """
        EQUIPMENT STATUS
        """

        await seed_if_empty(
            db,
            EquipmentStatus,
            [
                {"name": "Active"},
                {"name": "Under Repair"},
                {"name": "Out of Service"},
                {"name": "Installed"}
            ]
        )

        """
        MAINTENANCE TYPES
        """

        await seed_if_empty(
            db,
            MaintenanceType,
            [
                {"name": "Preventive"},
                {"name": "Corrective"},
                {"name": "Inspection"},
                {"name": "Emergency"}
            ]
        )

        """
        EQUIPMENT TYPES
        """

        result = await db.execute(
            select(EquipmentCategory)
        )

        categories = result.scalars().all()

        category_map = {
            c.name: c.id
            for c in categories
        }

        await seed_if_empty(
            db,
            EquipmentType,
            [
                {
                    "name": "Mini Split",
                    "category_id":
                        category_map[
                            "Air Conditioning"
                        ]
                },
                {
                    "name": "VRF",
                    "category_id":
                        category_map[
                            "Air Conditioning"
                        ]
                },
                {
                    "name": "Boiler",
                    "category_id":
                        category_map[
                            "Heating"
                        ]
                },
                {
                    "name": "Air Handler",
                    "category_id":
                        category_map[
                            "Ventilation"
                        ]
                },
                {
                    "name": "Fan Coil",
                    "category_id":
                        category_map[
                            "Ventilation"
                        ]
                }
            ]
        )

        print(
            'HVAC catalogs seeded successfully'
        )


if __name__ == '__main__':

    asyncio.run(run())