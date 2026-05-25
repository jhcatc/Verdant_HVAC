from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str