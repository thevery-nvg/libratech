from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str
    patronymic: str


class UserCreate(UserBase):
    password: str
    password_repeat: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None)
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None


class UserRead(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserAdminUpdate(UserUpdate):
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None


class RoleOut(BaseModel):
    id: int
    name: str
    permissions: List[str]

    class Config:
        from_attributes = True


class MeResponse(BaseModel):
    id: int
    email: str
    name: str | None
    surname: str | None
    patronymic: str | None
    roles: List[RoleOut]
    # permissions: List[str]