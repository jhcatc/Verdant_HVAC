from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import uuid
from datetime import datetime, timezone
from app.services.service_order_service import recalculate_order_cost
from app.core.database import get_db
from app.models.service_order import ServiceOrder
from app.models.service_order_task import ServiceOrderTask
from app.models.service_order_material import ServiceOrderMaterial
from app.models.service_order_log import ServiceOrderLog
from app.models.service_order_assignment import ServiceOrderAssignment
from sqlalchemy import delete
from app.services.service_order_service import (
    assign_and_schedule,
    rebalance_day_for_technician
)
from app.services.service_order_service import suggest_best_dispatch
from dateutil import parser
from app.models.user import User
from app.core.ws_manager import manager
from app.services.dispatch_ai_service import (
    suggest_best_technicians
)
from app.services.route_optimization_service import (
    build_routes,
    build_heatmap
)


router = APIRouter(prefix="/service-orders", tags=["Service Orders"])


# =========================================================
# 🔹 GET ALL
# =========================================================

@router.get("/")
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ServiceOrder).options(
            selectinload(ServiceOrder.customer),
            selectinload(ServiceOrder.customer_location),
            selectinload(ServiceOrder.equipment),
            selectinload(ServiceOrder.tasks),
            selectinload(ServiceOrder.materials),
            selectinload(ServiceOrder.logs),
            selectinload(ServiceOrder.maintenance_plan),
            selectinload(
                ServiceOrder.assignments
            ).selectinload(
                ServiceOrderAssignment.user
            ),
        )
    )
    return result.scalars().all()


# =========================================================
# 🔹 GET ONE
# =========================================================

@router.get("/{order_id}")
async def get_order(order_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ServiceOrder)
        .options(
            selectinload(ServiceOrder.tasks),
            selectinload(ServiceOrder.materials),
            selectinload(ServiceOrder.logs),
            selectinload(ServiceOrder.assignments).selectinload(ServiceOrderAssignment.user),
        )
        .where(ServiceOrder.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(404, "Order not found")

    return order


# =========================================================
# 🔹 CREATE
# =========================================================


@router.post("/")
async def create_order(data: dict, db: AsyncSession = Depends(get_db)):

    # 🔥 VALIDACIONES BASE
    if not data.get("title"):
        raise HTTPException(400, "title required")

    if not data.get("customer_id"):
        raise HTTPException(400, "customer_id required")

    # 🔥 FIX UUID
    try:
        customer_id = uuid.UUID(data["customer_id"])
    except:
        raise HTTPException(400, "Invalid customer_id")

    try:
        order = ServiceOrder(
            id=uuid.uuid4(),
            title=data["title"],
            customer_id=customer_id,
            customer_location_id=data.get(
                "customer_location_id"
            ),
            equipment_id=data.get(
                "equipment_id"
            ),
            city=data.get("city"),
            duration_hours=float(
                data.get("duration_hours", 1)
            ),
            labor_cost=float(
                data.get("labor_cost", 0)
            ),
            created_at=datetime.utcnow()
        )

        db.add(order)

        # 🔹 TASKS
        for t in data.get("tasks", []):
            if not t.get("title"):
                continue

            db.add(ServiceOrderTask(
                id=uuid.uuid4(),
                order_id=order.id,
                title=t["title"],
                description=t.get("description"),
            ))

        # 🔹 MATERIALS (LIMPIOS)
        for m in data.get("materials", []):
            if not m.get("inventory_item_id"):
                continue

            db.add(ServiceOrderMaterial(
                id=uuid.uuid4(),
                order_id=order.id,
                inventory_item_id=m.get("inventory_item_id"),
                name=m.get("name"),
                unit_cost=float(m.get("unit_cost", 0)),
                quantity=float(m.get("quantity", 0))
            ))

        # 🔹 LOG
        db.add(ServiceOrderLog(
            id=uuid.uuid4(),
            order_id=order.id,
            action="created",
            description="Order created",
            created_at=datetime.utcnow()
        ))

        # 🔥 IMPORTANTE: flush antes de usar order
        await db.flush()

        # 🔥 recargar relaciones correctamente
        result = await db.execute(
            select(ServiceOrder)
            .options(selectinload(ServiceOrder.materials))
            .where(ServiceOrder.id == order.id)
        )

        order_db = result.scalar_one()

        await recalculate_order_cost(db, order_db)

        await db.commit()

        return {
            "ok": True,
            "id": str(order.id)
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, str(e))
    
# =========================================================
# 🔴 PATCH DISPATCH (ÚNICO FLUJO REAL)
# =========================================================

@router.patch("/{order_id}/dispatch")
async def dispatch_order(order_id: str, data: dict, db: AsyncSession = Depends(get_db)):

    technician_id = data.get("technician_id")
    scheduled_at = data.get("scheduled_at")
    duration_hours = data.get("duration_hours", 1)

    if not technician_id:
        raise HTTPException(400, "technician_id required")

    # ✅ UUID
    try:
        technician_id = uuid.UUID(technician_id)
    except:
        raise HTTPException(400, "Invalid technician_id")

    # ✅ DATETIME
    scheduled_dt = None
    if scheduled_at:
        try:
            scheduled_dt = parser.isoparse(scheduled_at)

            if scheduled_dt.tzinfo is None:
                scheduled_dt = scheduled_dt.replace(tzinfo=timezone.utc)

        except Exception:
            raise HTTPException(400, f"Invalid datetime: {scheduled_at}")

    try:
        with db.no_autoflush:

            order = await assign_and_schedule(
                db,
                order_id,
                technician_id=technician_id,
                scheduled_at=scheduled_dt,
                duration_hours=duration_hours
            )

            if scheduled_dt:
                plan = await rebalance_day_for_technician(
                    db,
                    technician_id,
                    scheduled_dt,
                    new_order=order
                )

                for item in plan:
                    o = await db.get(ServiceOrder, item["order_id"])
                    o.scheduled_at = item["scheduled_at"]

        await db.commit()

        # 🔥🔥🔥 ESTE ES EL PUNTO CLAVE
        await manager.broadcast({
            "type": "order_status_changed",
            "order_id": str(order.id),
            "status": order.status  # ⚠️ IMPORTANTE: usa el valor real
        })

        return {"ok": True}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, str(e))
    
@router.get("/{order_id}/suggest")
async def suggest_dispatch(order_id: str, db: AsyncSession = Depends(get_db)):
    result = await suggest_best_dispatch(db, order_id)
    return result

@router.put("/{order_id}")
async def update_order(order_id: str, data: dict, db: AsyncSession = Depends(get_db)):

    order = await db.get(ServiceOrder, order_id)

    if not order:
        raise HTTPException(404, "Order not found")

    # 🔹 básicos
    order.title = data.get("title", order.title)
    order.city = data.get("city", order.city)
    order.labor_cost = data.get("labor_cost", order.labor_cost)

    # 🔹 limpiar materiales
    await db.execute(
        delete(ServiceOrderMaterial).where(
            ServiceOrderMaterial.order_id == order.id
        )
    )

    # 🔹 recrear materiales
    for m in data.get("materials", []):
        db.add(ServiceOrderMaterial(
            order_id=order.id,
            inventory_item_id=m.get("inventory_item_id"),
            name=m["name"],
            unit_cost=m.get("unit_cost", 0),
            quantity=m["quantity"]
        ))

    await db.flush()

    # 🔥 recalcular costo
    materials_total = sum(
        (m["quantity"] or 0) * (m.get("unit_cost", 0))
        for m in data.get("materials", [])
    )

    order.estimated_cost = materials_total + (order.labor_cost or 0)

    await db.commit()

    return {"ok": True}


@router.patch("/{order_id}/status")
async def update_status(order_id: str, data: dict, db: AsyncSession = Depends(get_db)):

    order = await db.get(ServiceOrder, order_id)

    if not order:
        raise HTTPException(404, "Order not found")

    order.status = data.get("status", order.status)

    db.add(ServiceOrderLog(
        order_id=order.id,
        action="status_changed",
        description=f"Status changed to {order.status}"
    ))

    await db.commit()

    return {"ok": True}

@router.patch("/{order_id}/start")
async def start_order(
    order_id: str,
    db: AsyncSession = Depends(get_db)
):

    order = await db.get(
        ServiceOrder,
        order_id
    )

    if not order:
        raise HTTPException(404, "Order not found")
    order.status = ServiceOrderStatus.IN_PROGRESS
    order.started_at = datetime.utcnow()
    db.add(

        ServiceOrderLog(

            id=uuid.uuid4(),
            order_id=order.id,
            action="work_started",
            description="Technician started work",
            created_at=datetime.utcnow()
        )
    )

    await db.commit()

    return {
        "ok": True
    }

# =========================================================
# 🤖 ENTERPRISE AI DISPATCH
# =========================================================

@router.get("/{order_id}/ai-dispatch")
async def ai_dispatch(
    order_id: str,
    db: AsyncSession = Depends(get_db)
):

    result = await suggest_best_technicians(
        db,
        order_id
    )

    return result

# =========================================================
# ROUTES
# =========================================================

@router.get("/routing/routes")
async def get_routes(
    db: AsyncSession = Depends(get_db)
):
    return await build_routes(db)


# =========================================================
# HEATMAP
# =========================================================

@router.get("/routing/heatmap")
async def get_heatmap(
    db: AsyncSession = Depends(get_db)
):
    return await build_heatmap(db)