from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import Column, Float, and_
from datetime import datetime, timedelta, timezone
import uuid
import json
from collections import defaultdict
from uuid import UUID
from app.core.redis import redis_client
from app.models.service_order import ServiceOrder, ServiceOrderStatus
from app.models.service_order_assignment import ServiceOrderAssignment
from app.models.service_order_log import ServiceOrderLog
from app.models.user import User
from app.services.invoice_service import generate_pdf, send_email
from app.services.inventory_service import consume_inventory
from app.models.user import User
from fastapi import HTTPException
from sqlalchemy.orm import noload
from zoneinfo import ZoneInfo


# =========================================================
# CONFIG
# =========================================================

SLOT_MINUTES = 15
BUFFER_MINUTES = 15

PRIORITY_MAP = {
    "low": 1,
    "medium": 2,
    "high": 3
}


# =========================================================
# HELPERS
# =========================================================

async def add_log(db: AsyncSession, order_id, action: str, description: str):
    db.add(ServiceOrderLog(
        id=uuid.uuid4(),
        order_id=order_id,
        action=action,
        description=description,
        created_at=datetime.utcnow()
    ))


async def publish_event(event: dict):
    await redis_client.publish("orders", json.dumps(event))


async def emit_order_event(order: ServiceOrder, event_type: str):
    await publish_event({
        "type": event_type,
        "order_id": str(order.id),
        "status": getattr(order, "status", None),
        "scheduled_at": order.scheduled_at.isoformat() if order.scheduled_at else None,
        "updated_at": datetime.utcnow().isoformat()
    })


# =========================================================
# TIME UTILS
# =========================================================

def round_to_slot(dt: datetime):
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)

    minute = (dt.minute // SLOT_MINUTES) * SLOT_MINUTES
    return dt.replace(minute=minute, second=0, microsecond=0)


def calculate_end(start: datetime, duration_hours: int):
    return start + timedelta(hours=duration_hours)


def add_buffer(end: datetime):
    return end + timedelta(minutes=BUFFER_MINUTES)


# =========================================================
# QUERY
# =========================================================

async def get_orders_in_range(db: AsyncSession, start: datetime, end: datetime):
    result = await db.execute(
        select(ServiceOrder).where(
            ServiceOrder.scheduled_at.between(start, end),
            ServiceOrder.is_active == True
        )
    )
    return result.scalars().all()


# =========================================================
# VALIDACIÓN
# =========================================================

async def validate_slot(db, technician_id, new_start, new_end, exclude_order_id=None):

    if not technician_id:
        raise HTTPException(400, "technician_id required")

    result = await db.execute(
        select(ServiceOrder)
        .join(ServiceOrderAssignment)
        .where(
            ServiceOrderAssignment.user_id == technician_id,
            ServiceOrder.is_active == True
        )
    )

    orders = result.scalars().unique().all()

    for o in orders:
        if exclude_order_id and str(o.id) == str(exclude_order_id):
            continue

        if not o.scheduled_at:
            continue

        existing_start = o.scheduled_at
        duration = getattr(o, "duration_hours", 1)

        existing_end = calculate_end(existing_start, duration)
        existing_end_with_buffer = add_buffer(existing_end)

        if new_start < existing_end_with_buffer and new_end > existing_start:
            raise HTTPException(400, "Time slot overlaps (with buffer)")

# =========================================================
# CREATE
# =========================================================

async def create_service_order(db: AsyncSession, data):
    order = ServiceOrder(**data.dict())

    db.add(order)
    await db.flush()

    await add_log(db, order.id, "created", "Order created")

    await db.commit()
    await db.refresh(order)

    await emit_order_event(order, "order_created")

    return order


# =========================================================
# UPDATE
# =========================================================

async def update_service_order(db: AsyncSession, order_id, updates):
    order = await db.get(ServiceOrder, order_id)

    for key, value in updates.dict(exclude_unset=True).items():
        setattr(order, key, value)

    await add_log(db, order_id, "updated", "Order updated")

    await db.commit()

    await emit_order_event(order, "order_updated")

    return order


# =========================================================
# STATUS
# =========================================================

async def update_status(db: AsyncSession, order_id, status):
    order = await db.get(ServiceOrder, order_id)

    order.status = status

    await add_log(db, order_id, "status_changed", f"Status changed to {status}")

    await db.commit()

    await emit_order_event(order, "order_status_changed")

    return order


# =========================================================
# NOTES
# =========================================================

async def add_note(db, order_id, note: str):
    await add_log(db, order_id, "note", note)

    await db.commit()

    await publish_event({
        "type": "order_note",
        "order_id": str(order_id),
        "description": note,
        "created_at": datetime.utcnow().isoformat()
    })


# =========================================================
# ASSIGN + SCHEDULE
# =========================================================

async def assign_and_schedule(db, order_id, technician_id=None, scheduled_at=None, duration_hours=1):

    # =====================================================
    # 🔒 LOCK ORDER (FIX REAL)
    # =====================================================

    result = await db.execute(
        select(ServiceOrder)
        .where(ServiceOrder.id == order_id)
        .with_for_update(of=ServiceOrder)
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(404, "Order not found")

    # =====================================================
    # 🔒 LOCK TECHNICIAN
    # =====================================================

    if technician_id:

        tech_result = await db.execute(
            select(User)
            .options(noload("*"))
            .where(User.id == technician_id)
            .with_for_update(of=User)
        )

        tech = tech_result.scalar_one_or_none()

        if not tech:
            raise HTTPException(404, "Technician not found")

    # =====================================================
    # ⏱️ NORMALIZE SLOT
    # =====================================================

    if scheduled_at:
        scheduled_at = round_to_slot(scheduled_at)

    # =====================================================
    # 🔍 VALIDATE OVERLAP
    # =====================================================

    if technician_id and scheduled_at:

        await validate_slot(
            db,
            technician_id,
            scheduled_at,
            calculate_end(scheduled_at, duration_hours),
            exclude_order_id=order_id
        )

    # =====================================================
    # 👤 ASSIGN TECHNICIAN
    # =====================================================

    if technician_id:

        await db.execute(
            ServiceOrderAssignment.__table__.delete().where(
                ServiceOrderAssignment.order_id == order_id
            )
        )

        db.add(
            ServiceOrderAssignment(
                id=uuid.uuid4(),
                order_id=order_id,
                user_id=technician_id,
                is_primary=True,
                assigned_at=datetime.utcnow()
            )
        )

        order.status = ServiceOrderStatus.ASSIGNED

    # =====================================================
    # 📅 SCHEDULE
    # =====================================================

    if scheduled_at:

        order.scheduled_at = scheduled_at
        order.duration_hours = duration_hours

        if technician_id:
            order.status = ServiceOrderStatus.ASSIGNED

    # =====================================================
    # 📝 LOG
    # =====================================================

    await add_log(
        db,
        order_id,
        "assigned",
        "Assigned & scheduled"
    )

    return order

# =========================================================
# COMPLETE
# =========================================================

async def complete_service_order(db, order_id):
    order = await db.get(ServiceOrder, order_id)

    async with db.begin():
        await consume_inventory(db, order_id=str(order.id), materials=order.materials)

        order.status = ServiceOrderStatus.completed
        order.completed_at = datetime.utcnow()

        await add_log(db, order_id, "completed", "Order completed")

    await emit_order_event(order, "order_completed")

    await handle_invoice(db, order)

    return order


# =========================================================
# INVOICE
# =========================================================

async def handle_invoice(db, order):
    pdf_path = await generate_pdf(order)
    await send_email(order.customer.email, pdf_path)

    await add_log(db, order.id, "invoice_sent", "Invoice sent")

    await db.commit()


# =========================================================
# REBALANCE (FIX PRIORITY)
# =========================================================

async def rebalance_day_for_technician(db, technician_id, target_date, new_order=None):
    if target_date.tzinfo is not None:
        target_date = target_date.astimezone(timezone.utc).replace(tzinfo=None)

    start_day = target_date.replace(hour=8, minute=0, second=0, microsecond=0)
    end_day = target_date.replace(hour=18, minute=0, second=0, microsecond=0)

    orders = await get_orders_in_range(db, start_day, end_day)

    tech_orders = []

    for o in orders:
        for a in o.assignments:
            if str(a.user_id) == str(technician_id):
                tech_orders.append(o)

    if new_order:
        tech_orders.append(new_order)

    # 🔥 FIX PRIORITY
    def get_priority(o):
        if not hasattr(o, "priority"):
            return 0
        return PRIORITY_MAP.get(o.priority, 0)

    tech_orders = [
        o for o in tech_orders
        if isinstance(o, ServiceOrder)
    ]

    tech_orders.sort(
        key=get_priority,
        reverse=True
    )

    current_time = start_day
    plan = []

    for o in tech_orders:
        duration = getattr(o, "duration_hours", 1)

        while True:
            end = calculate_end(current_time, duration)

            try:
                await validate_slot(db, technician_id, current_time, end, exclude_order_id=o.id)
                break
            except:
                current_time += timedelta(minutes=SLOT_MINUTES)

        plan.append({
            "order_id": str(o.id),
            "scheduled_at": current_time
        })

        current_time = add_buffer(end)

    return plan


# =========================================================
# SUGGEST (BASE)
# =========================================================

async def recalculate_order_cost(db, order):
    total_material = 0

    # 🔥 asegurar que materiales existen en sesión
    await db.flush()

    for m in order.materials or []:
        qty = m.quantity or 0
        cost = m.unit_cost or 0
        total_material += qty * cost

    labor = order.labor_cost or 0

    # 🔹 ESTIMADOS (por ahora igual a actual)
    order.estimated_material_cost = total_material
    order.estimated_labor_cost = labor
    order.estimated_cost = total_material + labor

    # 🔹 REALES
    order.actual_material_cost = total_material
    order.actual_labor_cost = labor
    order.actual_cost = total_material + labor

async def suggest_best_dispatch(db, order_id):
    technicians = await db.execute(
        select(User).where(User.is_active == True)
    )
    technicians = technicians.scalars().all()

    results = []

    for tech in technicians:
        count = await db.execute(
            select(ServiceOrderAssignment)
            .where(ServiceOrderAssignment.user_id == tech.id)
        )

        load = len(count.scalars().all())

        results.append({
            "technician_id": str(tech.id),
            "score": -load
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results