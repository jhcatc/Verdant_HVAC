import uuid

from app.models.crm.contract import Contract


async def create_contract_from_opportunity(db, opportunity):
    contract = Contract(
        id=uuid.uuid4(),
        customer_name=opportunity.company,
        status="ACTIVE",
        total_value=opportunity.estimated_value,
        sla_tier="STANDARD",
        start_date=None,
        end_date=None,
        renewal_date=None,
        version=1,
    )

    db.add(contract)
    await db.commit()
    await db.refresh(contract)
    return contract