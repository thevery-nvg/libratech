from typing import Iterable

from fastapi import HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.rbac.models import Role, Permission


async def get_role_by_name(
        session: AsyncSession,
        name: str,
) -> Role | None:
    stmt = select(Role).where(Role.name == name)
    return await session.scalar(stmt)


async def get_permission_by_code(
        session: AsyncSession,
        code: str,
) -> Permission | None:
    stmt = select(Permission).where(Permission.code == code)
    return await session.scalar(stmt)


async def create_role(
        session: AsyncSession,
        name: str,
        description: str | None,
        permission_codes: Iterable[str],
) -> Role:
    permissions = []

    for code in permission_codes:
        permission = await get_permission_by_code(session, code)
        if not permission:
            raise ValueError(f"Permission '{code}' does not exist")
        permissions.append(permission)

    role = Role(
        name=name,
        description=description,
        permissions=permissions,
    )

    session.add(role)
    await session.commit()
    await session.refresh(role)

    return role


async def assign_role_to_user(
    session: AsyncSession,
    user_id: int,
    role_id: int,
):
    user = await session.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role = await session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    if role in user.roles:
        return role

    user.roles.append(role)
    await session.commit()

    return role


async def remove_role_from_user(
        session: AsyncSession,
        user: User,
        role_name: str,
):
    role = await get_role_by_name(session, role_name)
    if not role:
        raise ValueError("Role not found")

    if role in user.roles:
        user.roles.remove(role)
        await session.commit()


async def user_has_permission(
        user: User,
        permission_code: str,
) -> bool:
    if not user.is_active:
        return False

    for role in user.roles:
        for permission in role.permissions:
            if permission.code == permission_code:
                return True

    return False


async def get_user_with_role(session: AsyncSession, user_id: int):
    result = await session.execute(
        select(User.email, Role.name.label('role_name'))
        .join(User.roles)
        .where(User.id == user_id)
    )
    return result.first()