from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.customer_location import CustomerLocation
from app.models.customer import Customer

from app.schemas.customer_location import (
    CustomerLocationCreate
)


async def create_location(
    db: AsyncSession,
    data: CustomerLocationCreate
):
    location = CustomerLocation(
        **data.model_dump()
    )

    db.add(location)

    await db.commit()
    await db.refresh(location)

    return {
        "id": str(location.id),
        "customer_id": str(location.customer_id),
        "name": location.name,
        "code": location.code,
        "location_type": location.location_type,
        "address": location.address,
        "city": location.city,
        "state": location.state,
        "zip_code": location.zip_code,
        "country": location.country,
        "contact_name": location.contact_name,
        "contact_phone": location.contact_phone,
        "contact_email": location.contact_email,
        "sla_tier": location.sla_tier,
        "access_notes": location.access_notes,
        "refrigerant_notes": location.refrigerant_notes,
        "technician_notes": location.technician_notes,
        "notes": location.notes
    }


async def get_locations(
    db: AsyncSession
):
    result = await db.execute(
        select(CustomerLocation)
        .options(
            selectinload(CustomerLocation.customer)
        )
        .order_by(CustomerLocation.name)
    )

    locations = result.scalars().all()

    return [
        {
            "id": str(location.id),
            "customer_id": str(location.customer_id),
            "customer_name": (
                location.customer.name
                if location.customer else None
            ),
            "name": location.name,
            "code": location.code,
            "location_type": location.location_type,
            "address": location.address,
            "city": location.city,
            "state": location.state,
            "zip_code": location.zip_code,
            "country": location.country,
            "contact_name": location.contact_name,
            "contact_phone": location.contact_phone,
            "contact_email": location.contact_email,
            "sla_tier": location.sla_tier,
            "access_notes": location.access_notes,
            "refrigerant_notes": location.refrigerant_notes,
            "technician_notes": location.technician_notes,
            "notes": location.notes,
            "is_active": location.is_active
        }
        for location in locations
    ]

async def get_customer_locations(
    db: AsyncSession,
    customer_id
):
    result = await db.execute(
        select(CustomerLocation)
        .where(
            CustomerLocation.customer_id == customer_id
        )
        .order_by(CustomerLocation.name)
    )

    locations = result.scalars().all()

    return [
        {
            "id": str(location.id),
            "customer_id": str(location.customer_id),
            "name": location.name,
            "code": location.code,
            "location_type": location.location_type,
            "address": location.address,
            "city": location.city,
            "state": location.state,
            "zip_code": location.zip_code,
            "country": location.country,
            "contact_name": location.contact_name,
            "contact_phone": location.contact_phone,
            "contact_email": location.contact_email,
            "sla_tier": location.sla_tier,
            "access_notes": location.access_notes,
            "refrigerant_notes": location.refrigerant_notes,
            "technician_notes": location.technician_notes,
            "notes": location.notes,
            "is_active": location.is_active
        }
        for location in locations
    ]