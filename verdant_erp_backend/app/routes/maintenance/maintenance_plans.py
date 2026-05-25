import uuid
from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.maintenance.maintenance_plan import (
    MaintenancePlan
)
from app.models.maintenance.maintenance_plan_equipment import (
    MaintenancePlanEquipment
)
from app.models.maintenance.maintenance_task_template import (
    MaintenanceTaskTemplate
)

router = APIRouter(
    prefix="/maintenance-plans",
    tags=["maintenance-plans"]
)


@router.get("/")
async def get_plans(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MaintenancePlan)

        .options(
            selectinload(
                MaintenancePlan.equipment
            ).selectinload(
                MaintenancePlanEquipment.equipment
            ),
            selectinload(
                MaintenancePlan.task_templates
            )
        )
    )

    return result.scalars().unique().all()


@router.post("/")
async def create_plan(
    data: dict,
    db: AsyncSession = Depends(get_db)
):
    plan = MaintenancePlan(
        id=uuid.uuid4(),
        customer_id=data["customer_id"],
        location_id=data["location_id"],
        name=data["name"],
        description=data.get(
            "description"
        ),
        frequency_days=data[
            "frequency_days"
        ],
        start_date=data[
            "start_date"
        ],
        next_run_date=data[
            "start_date"
        ]
    )

    db.add(plan)

    await db.flush()

    """
    EQUIPMENT
    """

    for equipment_id in data.get(
        "equipment_ids",
        []
    ):
        db.add(
            MaintenancePlanEquipment(
                id=uuid.uuid4(),
                maintenance_plan_id=plan.id,
                equipment_id=equipment_id
            )
        )

    """
    TASKS
    """

    for task in data.get(
        "tasks",
        []
    ):

        db.add(
            MaintenanceTaskTemplate(
                id=uuid.uuid4(),
                maintenance_plan_id=plan.id,
                title=task["title"],
                description=task.get(
                    "description"
                )
            )
        )

    await db.commit()

    return {
        "ok": True,
        "id": str(plan.id)
    }