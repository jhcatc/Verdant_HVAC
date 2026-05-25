from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.hvac.equipment_component import (
    EquipmentComponent
)


async def get_component_registry_snapshot(db):

    query = (
        select(EquipmentComponent)
        .options(
            joinedload(
                EquipmentComponent.equipment
            )
        )
    )

    result = await db.execute(query)
    rows = result.scalars().all()
    items = []
    for component in rows:

        health_score = 100
        if component.status.lower() != "active":
            health_score -= 40
        if component.failure_reason:
            health_score -= 20
        if component.is_critical:
            health_score -= 10
        health_score = max(0, health_score)
        warranty_status = "active"
        if component.warranty_expiration:
            if component.warranty_expiration < date.today():
                warranty_status = "expired"
        failure_events = 0
        if component.failure_reason:
            failure_events = 1
        mtbf_days = None
        if (
            component.installation_date
            and component.replacement_date
        ):
            mtbf_days = (
                component.replacement_date
                - component.installation_date
            ).days
        items.append({
            "id": component.id,
            "equipment_id":
                component.equipment_id,
            "component_type":
                component.component_type,
            "component_name":
                component.component_name,
            "manufacturer":
                component.manufacturer,
            "model_number":
                component.model_number,
            "serial_number":
                component.serial_number,
            "status":
                component.status,
            "installation_date":
                component.installation_date,
            "replacement_date":
                component.replacement_date,
            "warranty_expiration":
                component.warranty_expiration,
            "useful_life_months":
                component.useful_life_months,
            "failure_reason":
                component.failure_reason,
            "replacement_reason":
                component.replacement_reason,
            "notes":
                component.notes,
            "is_critical":
                component.is_critical,
            "maintenance_log_id":
                component.maintenance_log_id,
            "created_at":
                component.created_at,
            "equipment_asset_tag":
                component.equipment.asset_tag
                if component.equipment else None,
            "equipment_model":
                component.equipment.model
                if component.equipment else None,
            "health_score":
                health_score,
            "warranty_status":
                warranty_status,
            "mtbf_days":
                mtbf_days,
            "failure_events":
                failure_events
        })

    return {

        "total_components":
            len(items),
        "critical_components":
            len([
                x for x in items
                if x["is_critical"]
            ]),
        "failed_components":
            len([
                x for x in items
                if x["status"] != "active"
            ]),
        "warranty_expiring":
            len([
                x for x in items
                if x["warranty_status"]
                == "expired"
            ]),
        "average_health_score":
            int(
                sum([
                    x["health_score"]
                    for x in items
                ]) / len(items)
            ) if items else 0,

        "items":
            items
    }