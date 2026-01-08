from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.core.db.manager import db_manager
from . import schemas, service
from .models import User
from .security import create_access_token
from .dependencies import get_current_user
from ..rbac.models import Role

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
user_router = APIRouter(prefix="/user", tags=["User"])


@auth_router.post(
    "/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
        payload: schemas.UserCreate,
        session: AsyncSession = Depends(db_manager.get_async_session),
):
    try:
        user = await service.register_user(session, payload)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@auth_router.post(
    "/login",
    response_model=schemas.Token,
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(db_manager.get_async_session),
):
    user = await service.authenticate_user(
        session,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(subject=user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@auth_router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
        current_user=Depends(get_current_user), ):
    return


@user_router.get(
    "/me",
    response_model=schemas.MeResponse,
)
async def me(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(db_manager.get_async_session),
):
    stmt = (
        select(User)
        .where(User.id == current_user.id)
        .options(
            selectinload(User.roles)
            .selectinload(Role.permissions)
        )
    )

    result = await session.execute(stmt)
    user = result.scalar_one()

    roles_out = []
    permissions_set = set()

    for role in user.roles:
        role_permissions = [p.code for p in role.permissions]
        permissions_set.update(role_permissions)

        roles_out.append({
            "id": role.id,
            "name": role.name,
            "permissions": role_permissions,
        })

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "patronymic": user.patronymic,
        "roles": roles_out,
        "permissions": sorted(permissions_set),
    }


@user_router.patch(
    "/me",
    response_model=schemas.UserRead,
)
async def update_me(
        payload: schemas.UserUpdate,
        session: AsyncSession = Depends(db_manager.get_async_session),
        current_user=Depends(get_current_user),
):
    updated_user = await service.update_user(
        session=session,
        user=current_user,
        data=payload,
    )

    return updated_user


@user_router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_me(
        session: AsyncSession = Depends(db_manager.get_async_session),
        current_user=Depends(get_current_user),
):
    await service.deactivate_user(
        session=session,
        user=current_user,
    )

    return
