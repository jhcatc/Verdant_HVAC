from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.customer_location import (
    CustomerLocationCreate
)
from app.services.customer_location_service import (
    create_location,
    get_locations,
    get_customer_locations
)

router = APIRouter(
    prefix="/customer-locations",
    tags=["customer-locations"]
)


@router.post("/")
async def create_customer_location(
    data: CustomerLocationCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_location(db, data)


@router.get("/")
async def list_locations(
    db: AsyncSession = Depends(get_db)
):
    return await get_locations(db)


@router.get("/customer/{customer_id}")
async def list_customer_locations(
    customer_id,
    db: AsyncSession = Depends(get_db)
):
    return await get_customer_locations(
        db,
        customer_id
    )