from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.core.database import get_db
from app.deps import get_current_user
from app.models.inventory_item import InventoryItem
from app.models.inventory_movement import InventoryMovement
from app.models.location import Location
from app.models.adjustment_request import AdjustmentRequest

from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemOut
)
from app.services.inventory_service import (
    list_inventory,
    get_inventory_item,
    update_inventory_item,
    add_stock,
    remove_stock,
    transfer_inventory,
    get_inventory_grid,
    get_ira_report,
    create_inventory_item
)

router = APIRouter(prefix="/inventory", tags=["inventory"])


# =========================
# CREATE ITEM ✅
# =========================
@router.post("/", response_model=InventoryItemOut)
async def create_item(
    data: InventoryItemCreate,
    db: AsyncSession = Depends(get_db)
):
    item = InventoryItem(**data.dict())

    db.add(item)
    await db.commit()
    await db.refresh(item)

    # 🔥 FIX CLAVE: convertir UUID a string
    return {
        "id": str(item.id),
        "name": item.name,
        "sku": item.sku,
        "category": item.category,
        "unit_cost": item.unit_cost,
        "stock": item.stock,
    }


# =========================
# LIST
# =========================

@router.get("/")
async def list_items(
    q: str = None,
    category: str = None,
    low_stock: bool = False,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    return await list_inventory(
        db,
        q=q,
        category=category,
        low_stock=low_stock,
        limit=limit,
        offset=offset
    )

# =========================
# UPDATE
# =========================
@router.patch("/{item_id}")
async def update_item(
    item_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db)
):
    return await update_inventory_item(db, item_id, payload)


# =========================
# STOCK IN
# =========================
@router.post("/{item_id}/add-stock")
async def add_stock_route(
    item_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await add_stock(
        db,
        item_id,
        payload.get("quantity"),
        payload.get("location_id"),
        user.id,
        payload.get("reason", "manual")
    )


# =========================
# STOCK OUT
# =========================
@router.post("/{item_id}/remove-stock")
async def remove_stock_route(
    item_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    return await remove_stock(
        db,
        item_id,
        payload.get("quantity"),
        payload.get("location_id"),
        user.id,
        payload.get("reason", "manual")
    )


# =========================
# LOCATIONS
# =========================
@router.get("/locations")
async def get_locations(db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(Location))).scalars().all()


@router.post("/locations")
async def create_location(data: dict, db: AsyncSession = Depends(get_db)):
    loc = Location(**data)
    db.add(loc)
    await db.commit()
    return loc


# =========================
# TRANSFER
# =========================
@router.post("/transfer")
async def transfer(
    data: dict,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    await transfer_inventory(
        db,
        data["item_id"],
        data["from_location"],
        data["to_location"],
        data["quantity"],
        user.id
    )
    return {"ok": True}


# =========================
# SEARCH
# =========================
@router.get("/search")
async def search_inventory(q: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InventoryItem)
        .where(InventoryItem.name.ilike(f"%{q}%"))
        .limit(10)
    )
    return result.scalars().all()


# =========================
# GRID
# =========================
@router.get("/grid")
@router.get("/grid/")
async def inventory_grid(db: AsyncSession = Depends(get_db)):
    return await get_inventory_grid(db)


# =========================
# IRA
# =========================
@router.get("/ira")
@router.get("/ira/")
async def inventory_ira(db: AsyncSession = Depends(get_db)):
    return await get_ira_report(db)


# =========================
# MOVEMENTS
# =========================
@router.get("/movements")
@router.get("/movements/")
async def list_movements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InventoryMovement).order_by(InventoryMovement.created_at.desc())
    )
    return result.scalars().all()


# =========================
# ADJUSTMENTS
# =========================
@router.get("/adjustments")
@router.get("/adjustments/")
async def adjustments(db: AsyncSession = Depends(get_db)):
    return (await db.execute(select(AdjustmentRequest))).scalars().all()


# =========================
# GET BY ID (SIEMPRE AL FINAL)
# =========================
@router.get("/{item_id}")
async def get_item(
    item_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await get_inventory_item(db, item_id)