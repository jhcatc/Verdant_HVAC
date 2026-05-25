from fastapi import FastAPI, HTTPException
from sqlalchemy.future import select
from app.models.user import User
from app.models.token import RefreshToken
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.role import Role
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

async def register_user(db: AsyncSession, data):
    role_name = data.role or "technician"

    result = await db.execute(
        select(Role).where(Role.name == role_name)
    )
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password[:72]),  # 🔥 fix bcrypt
        full_name=data.full_name,
        role_id=role.id
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def authenticate_user(db, email, password):
    result = await db.execute(
        select(User)
        .options(selectinload(User.role).selectinload(Role.permissions))
        .where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if not user:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user  # 👈 ESTO es clave