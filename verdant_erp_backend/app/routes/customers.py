from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.customer import Customer
from app.models.customer_contact import CustomerContact
from app.models.customer_address import CustomerAddress

import uuid

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# =========================================================
# LIST ALL
# =========================================================

@router.get("/")
async def list_customers(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Customer)
    )

    customers = result.scalars().all()

    return [
        {
            "id": str(c.id),
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "city": c.city
        }
        for c in customers
    ]


# =========================================================
# SEARCH
# =========================================================

@router.get("/search")
async def search_customers(
    q: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Customer)
        .where(Customer.name.ilike(f"%{q}%"))
        .limit(10)
    )

    customers = result.scalars().all()

    return [
        {
            "id": str(c.id),
            "name": c.name,
            "city": c.city,
            "phone": c.phone
        }
        for c in customers
    ]


# =========================================================
# CREATE
# =========================================================

@router.post("/")
async def create_customer(
    data: dict,
    db: AsyncSession = Depends(get_db)
):
    customer = Customer(
        id=uuid.uuid4(),
        name=data["name"],
        email=data.get("email"),
        phone=data.get("phone"),
        city=data.get("city")
    )

    db.add(customer)

    await db.commit()
    await db.refresh(customer)

    return {
        "id": str(customer.id),
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "city": customer.city
    }


# =========================================================
# CUSTOMER DETAIL
# =========================================================

@router.get("/{customer_id}")
async def customer_detail(
    customer_id: str,
    db: AsyncSession = Depends(get_db)
):

    customer = await db.get(
        Customer,
        customer_id
    )

    contacts_result = await db.execute(
        select(CustomerContact).where(
            CustomerContact.customer_id == customer_id
        )
    )

    addresses_result = await db.execute(
        select(CustomerAddress).where(
            CustomerAddress.customer_id == customer_id
        )
    )

    contacts = contacts_result.scalars().all()
    addresses = addresses_result.scalars().all()

    return {
        "id": str(customer.id),
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "city": customer.city,

        "contacts": [
            {
                "id": str(c.id),
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "role": c.role
            }
            for c in contacts
        ],

        "addresses": [
            {
                "id": str(a.id),
                "label": a.label,
                "address": a.address,
                "city": a.city
            }
            for a in addresses
        ],

        # TEMPORAL
        "notes": [],

        # TEMPORAL
        "orders": []
    }


# =========================================================
# CUSTOMER ORDERS
# TEMPORAL PLACEHOLDER
# =========================================================

@router.get("/{customer_id}/orders")
async def customer_orders(
    customer_id: str,
    db: AsyncSession = Depends(get_db)
):
    return []

@router.get("/search")
async def search_customers(
    q: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Customer)
        .where(
            Customer.name.ilike(f"%{q}%")
        )
        .limit(15)
    )
    customers = result.scalars().all()
    return customers