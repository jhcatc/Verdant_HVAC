from fastapi import APIRouter, Depends
from app.core.security import require_permission
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/technicians")
async def get_technicians(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User).where(User.is_active == True)
    )

    users = result.scalars().all()

    return [
        {
            "id": str(u.id),
            "name": u.full_name
        }
        for u in users
    ]

@router.get("/")
async def get_users(user = Depends(require_permission("users.read"))):
    return {"message": "You can see users"}