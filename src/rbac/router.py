from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.db.manager import db_manager
from src.rbac import schemas, service
from src.rbac.dependencies import require_permission
from src.rbac.permissions import *

rbac_router = APIRouter(
    prefix="/roles",
    tags=["RBAC / Roles"],
)


@rbac_router.get(
    "",
    response_model=list[schemas.RoleRead],
    dependencies=[Depends(require_permission(ROLE_READ))],

)
async def list_roles(
        session: AsyncSession = Depends(db_manager.get_async_session),
):
    stmt = select(service.Role)
    return (await session.scalars(stmt)).all()


@rbac_router.post(
    "",
    response_model=schemas.RoleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(DEV))],

)
async def create_role(
        payload: schemas.RoleCreate,
        session: AsyncSession = Depends(db_manager.get_async_session),
):
    try:
        return await service.create_role(
            session,
            name=payload.name,
            description=payload.description,
            permission_codes=payload.permissions,
        )
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(e))


@rbac_router.put(
    "/{role_name}",
    response_model=schemas.RoleRead,
    dependencies=[Depends(require_permission(DEV))],

)
async def update_role(
        role_name: str,
        payload: schemas.RoleUpdate,
        session: AsyncSession = Depends(db_manager.get_async_session),
):
    role = await service.get_role_by_name(session, role_name)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if payload.name is not None:
        role.name = payload.name

    if payload.description is not None:
        role.description = payload.description

    if payload.permissions is not None:
        role.permissions.clear()
        for code in payload.permissions:
            permission = await service.get_permission_by_code(session, code)
            if not permission:
                raise HTTPException(400, f"Permission '{code}' not found")
            role.permissions.append(permission)

    await session.commit()
    await session.refresh(role)
    return role


@rbac_router.post(
    "/assign-role",
    response_model=schemas.AssignRoleResponse,
    dependencies=[Depends(require_permission(ROLE_ASSIGN))],
)
async def assign_role(
        payload: schemas.AssignRoleRequest,
        session: AsyncSession = Depends(db_manager.get_async_session),
):
    role = await service.assign_role_to_user(
        session=session,
        user_id=payload.user_id,
        role_id=payload.role_id,
    )

    return {
        "status": "ok",
        "user_id": payload.user_id,
        "role": role.name,
    }


@rbac_router.delete(
    "/{role_name}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission(ROLE_DELETE))],
)
async def delete_role(
        role_name: str,
        session: AsyncSession = Depends(db_manager.get_async_session),

):
    role = await service.get_role_by_name(session, role_name)
    if not role:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    await session.delete(role)
    await session.commit()


