from fastapi import APIRouter, Depends, HTTPException, Body, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import register_user, authenticate_user
from app.deps import get_current_user
from app.core.database import get_db
from app.schemas.user import UserCreate
from app.schemas.auth import LoginSchema
from fastapi import Request
from app.core.security import create_access_token, create_refresh_token, decode_refresh_token
from jose import jwt

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        user = await register_user(db, data)
        return {"msg": "User created", "id": str(user.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(
    data: LoginSchema,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )

    return {"access_token": access_token}

@router.get("/me")
async def me(user = Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
        "full_name": user.full_name,  # ✅ FIX
        "role": {
            "id": user.role.id,
            "name": user.role.name
        },
        "permissions": [p.name for p in user.role.permissions]
    }

@router.post("/refresh")
async def refresh(request: Request):
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(status_code=401)

    payload = decode_refresh_token(token)
    new_access = create_access_token({"sub": payload["sub"]})

    return {"access_token": new_access}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}