from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.dependencies import get_current_user
from src.auth.models import User
from src.core.db.manager import db_manager
from src.rbac.models import Role


def require_permission(permission_code: str):
    async def dependency(
            user: User = Depends(get_current_user),
            session: AsyncSession = Depends(db_manager.get_async_session),
    ):
        stmt = (
            select(User)
            .where(User.id == user.id)
            .options(

                selectinload(User.roles).selectinload(Role.permissions)
            )
        )

        result = await session.execute(stmt)
        user = result.scalar_one()

        permissions = {
            perm.code
            for role in user.roles
            for perm in role.permissions
        }

        if permission_code not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_code}' required",
            )

        return user

    return dependency
