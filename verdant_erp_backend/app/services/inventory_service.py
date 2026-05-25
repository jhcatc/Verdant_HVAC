from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException
from app.models.inventory_item import InventoryItem
from app.models.inventory_movement import InventoryMovement
from app.models.inventory_stock import InventoryStock
from app.models.adjustment_request import AdjustmentRequest
from collections import defaultdict
from app.models.location import Location
from datetime import datetime, timedelta
from sqlalchemy import select
from app.models.inventory_item import InventoryItem

# =========================================================
# 🔹 GET ITEM
# =========================================================

async def get_inventory_item(db: AsyncSession, item_id: str):
    result = await db.execute(
        select(InventoryItem).where(InventoryItem.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(404, "Inventory item not found")

    return item


# =========================================================
# 🔹 LIST (COMPATIBLE)
# =========================================================

async def list_inventory(
    db: AsyncSession,
    q: str = None,
    category: str = None,
    low_stock: bool = False,
    limit: int = 20,
    offset: int = 0
):
    query = select(InventoryItem)

    conditions = []

    if q:
        conditions.append(InventoryItem.name.ilike(f"%{q}%"))

    if category:
        conditions.append(InventoryItem.category == category)

    if low_stock:
        conditions.append(InventoryItem.stock <= InventoryItem.min_stock)

    if conditions:
        query = query.where(and_(*conditions))

    # 🔥 total count
    total_result = await db.execute(query)
    total = len(total_result.scalars().all())

    # 🔥 paginated query
    result = await db.execute(
        query.order_by(InventoryItem.name)
        .limit(limit)
        .offset(offset)
    )

    items = result.scalars().all()

    return {
        "items": items,
        "total": total
    }

# =========================================================
# 🔹 STOCK POR LOCATION (NUEVO CORE)
# =========================================================

async def get_stock(db: AsyncSession, item_id, location_id):
    result = await db.execute(
        select(InventoryStock).where(
            InventoryStock.item_id == item_id,
            InventoryStock.location_id == location_id
        )
    )
    stock = result.scalar_one_or_none()

    if not stock:
        stock = InventoryStock(
            item_id=item_id,
            location_id=location_id,
            quantity=0
        )
        db.add(stock)
        await db.flush()

    return stock


# =========================================================
# 🔹 UPDATE ITEM
# =========================================================

async def update_inventory_item(db: AsyncSession, item_id: str, data: dict):
    async with db.begin():

        item = await db.get(
            InventoryItem,
            item_id,
            with_for_update=True
        )

        if not item:
            raise HTTPException(404, "Item not found")

        for key, value in data.items():
            setattr(item, key, value)

    return item


# =========================================================
# 🔹 STOCK IN (WAREHOUSE)
# =========================================================

async def add_stock(
    db: AsyncSession,
    item_id: str,
    quantity: float,
    location_id: str,
    user_id: str,
    reason: str = "manual"
):
    async with db.begin():

        item = await db.get(
            InventoryItem,
            item_id,
            with_for_update=True
        )

        stock = await get_stock(db, item_id, location_id)

        stock.quantity += quantity

        # 🔥 mantener compatibilidad global
        item.stock += quantity

        movement = InventoryMovement(
            item_id=item.id,
            to_location_id=location_id,
            quantity=quantity,
            type="in",
            reference=reason,
            performed_by=user_id
        )

        db.add(movement)

    return item


# =========================================================
# 🔹 STOCK OUT
# =========================================================

async def remove_stock(
    db: AsyncSession,
    item_id: str,
    quantity: float,
    location_id: str,
    user_id: str,
    reason: str = "manual"
):
    async with db.begin():

        item = await db.get(
            InventoryItem,
            item_id,
            with_for_update=True
        )

        stock = await get_stock(db, item_id, location_id)

        if stock.quantity < quantity:
            raise HTTPException(400, "Insufficient stock")

        stock.quantity -= quantity
        item.stock -= quantity  # 🔥 compatibilidad

        movement = InventoryMovement(
            item_id=item.id,
            from_location_id=location_id,
            quantity=quantity,
            type="out",
            reference=reason,
            performed_by=user_id
        )

        db.add(movement)

    return item


# =========================================================
# 🔹 TRANSFER (WAREHOUSE → VAN)
# =========================================================

async def transfer_inventory(
    db: AsyncSession,
    item_id,
    from_location,
    to_location,
    quantity,
    user_id
):
    async with db.begin():

        from_stock = await get_stock(db, item_id, from_location)
        to_stock = await get_stock(db, item_id, to_location)

        if from_stock.quantity < quantity:
            raise HTTPException(400, "Insufficient stock")

        from_stock.quantity -= quantity
        to_stock.quantity += quantity

        movement = InventoryMovement(
            item_id=item_id,
            from_location_id=from_location,
            to_location_id=to_location,
            quantity=quantity,
            type="transfer",
            performed_by=user_id
        )

        db.add(movement)


# =========================================================
# 🔹 REQUEST ADJUSTMENT
# =========================================================

async def request_adjustment(
    db: AsyncSession,
    item_id,
    location_id,
    quantity,
    reason,
    user_id
):
    req = AdjustmentRequest(
        item_id=item_id,
        location_id=location_id,
        quantity=quantity,
        reason=reason,
        requested_by=user_id
    )

    db.add(req)
    await db.commit()

    return req


# =========================================================
# 🔹 APPLY ADJUSTMENT (ADMIN)
# =========================================================

async def apply_adjustment(
    db: AsyncSession,
    request_id,
    approver_id
):
    async with db.begin():

        req = await db.get(AdjustmentRequest, request_id)

        if not req:
            raise HTTPException(404, "Request not found")

        if req.status != "pending":
            raise HTTPException(400, "Already processed")

        stock = await get_stock(db, req.item_id, req.location_id)

        stock.quantity += req.quantity

        movement = InventoryMovement(
            item_id=req.item_id,
            to_location_id=req.location_id,
            quantity=req.quantity,
            type="adjustment",
            performed_by=approver_id,
            reference=str(req.id)
        )

        db.add(movement)

        req.status = "approved"
        req.approved_by = approver_id


# =========================================================
# 🔹 CONSUMO (ORDERS) — AHORA POR LOCATION
# =========================================================

async def consume_inventory(
    db: AsyncSession,
    order_id: str,
    materials: list,
    location_id: str  # 🔥 VAN
):
    async with db.begin():

        for m in materials:

            item = await db.get(
                InventoryItem,
                m.inventory_item_id,
                with_for_update=True
            )

            stock = await get_stock(db, item.id, location_id)

            if stock.quantity < m.quantity:
                raise HTTPException(
                    400,
                    f"Insufficient stock for {item.name}"
                )

            stock.quantity -= m.quantity
            item.stock -= m.quantity

            db.add(InventoryMovement(
                item_id=item.id,
                from_location_id=location_id,
                quantity=m.quantity,
                type="out",
                reference=f"order:{order_id}"
            ))


async def get_ira_report(db: AsyncSession):
    from collections import defaultdict
    from datetime import datetime, timedelta

    from app.models.inventory_movement import InventoryMovement
    from app.models.location import Location
    from app.models.inventory_stock import InventoryStock

    # 🔹 locations
    locs = (await db.execute(select(Location))).scalars().all()

    # 🔹 movimientos últimos 30 días
    since = datetime.utcnow() - timedelta(days=30)

    movements = (await db.execute(
        select(InventoryMovement).where(
            InventoryMovement.created_at >= since
        )
    )).scalars().all()

    # 🔹 consumo
    consumption = defaultdict(float)

    for m in movements:
        if m.type == "out" and m.from_location_id:
            consumption[str(m.from_location_id)] += abs(m.quantity)

    # 🔹 stock actual
    stocks = (await db.execute(select(InventoryStock))).scalars().all()

    stock_map = defaultdict(float)
    for s in stocks:
        stock_map[str(s.location_id)] += s.quantity

    # 🔹 construir resultado SIEMPRE
    result = []

    for l in locs:
        loc_id = str(l.id)

        current_stock = stock_map.get(loc_id, 0)
        cons = consumption.get(loc_id, 0)

        ira = cons / current_stock if current_stock > 0 else 0

        result.append({
            "location_id": loc_id,
            "name": l.name,
            "code": l.code,
            "type": l.type,
            "consumption_30d": cons,
            "stock": current_stock,
            "ira": round(ira, 2)
        })

    return result

# =========================================================
# 🔹 IRA CALCULATION (SIMPLE VERSION)
# =========================================================

async def get_ira_by_location(db: AsyncSession):
    result = await db.execute(
        select(
            InventoryMovement.to_location_id,
            InventoryMovement.quantity
        )
    )

    movements = result.all()

    ira_map = defaultdict(float)

    for loc_id, qty in movements:
        if loc_id:
            ira_map[str(loc_id)] += abs(qty)

    return ira_map


# =========================================================
# 🔹 INVENTORY GRID (FIXED)
# =========================================================

async def get_inventory_grid(db: AsyncSession):

    items_result = await db.execute(
        select(InventoryItem).order_by(InventoryItem.name)
    )
    items = items_result.scalars().all()

    locations_result = await db.execute(
        select(Location)
    )
    locations = locations_result.scalars().all()

    stock_result = await db.execute(select(InventoryStock))
    stocks = stock_result.scalars().all()

    stock_map = {
        (str(s.item_id), str(s.location_id)): s.quantity
        for s in stocks
    }

    ira_map = await get_ira_by_location(db)

    grid = []

    for item in items:

        total_stock = 0

        for loc in locations:
            qty = stock_map.get((str(item.id), str(loc.id)), 0)
            total_stock += qty

        row["locations"].append({
            "location_id": str(loc.id),
            "location_name": loc.name,
            "quantity": qty,
            "ira": ira_map.get(str(loc.id), 0)
        })

        row["stock"] = total_stock  # 🔥 TOTAL GLOBAL

        grid.append(row)

    return {
        "items": grid,
        "locations": [
            {
                "id": str(l.id),
                "name": l.name,
                "type": l.type,
                "stock": total_stock,
                "min_stock": float(item.min_stock or 0)
            }
            for l in locations
        ]
    }

async def create_inventory_item(db, data):
    item = InventoryItem(**data.dict())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item