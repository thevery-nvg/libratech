from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.tables import role_permissions
from src.rbac.models import Role, Permission
from src.rbac.permissions import *


async def seed_permissions(session: AsyncSession) -> dict[str, Permission]:
    unique_codes: set[str] = set()

    for permissions in ROLE_PERMISSIONS.values():
        unique_codes.update(permissions)

    permissions_map: dict[str, Permission] = {}

    for code in unique_codes:
        permission = await session.scalar(
            select(Permission).where(Permission.code == code)
        )
        if not permission:
            permission = Permission(code=code)
            session.add(permission)

        permissions_map[code] = permission

    await session.commit()
    return permissions_map


async def seed_roles(
        session: AsyncSession,
        permissions_map: dict[str, Permission],
):
    for role_name, permission_codes in ROLE_PERMISSIONS.items():
        result = await session.execute(
            select(Role).where(Role.name == role_name)
        )
        role = result.scalar_one_or_none()

        if not role:
            role = Role(
                name=role_name,
                description=f"System role: {role_name}",
            )
            session.add(role)
            await session.flush()

        await session.execute(
            role_permissions.delete().where(
                role_permissions.c.role_id == role.id
            )
        )

        for code in permission_codes:
            if code in permissions_map:
                permission = permissions_map[code]
                await session.execute(
                    role_permissions.insert().values(
                        role_id=role.id,
                        permission_id=permission.id
                    )
                )

    await session.commit()


async def seed_rbac(session: AsyncSession):
    permissions_map = await seed_permissions(session)
    await seed_roles(session, permissions_map)
