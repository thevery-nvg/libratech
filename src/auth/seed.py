from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.manager import db_manager
from src.rbac.dependencies import require_permission
from .seed_data import seed_users

auth_dev_router = APIRouter(
    prefix="/dev_auth",
    tags=["DEV_AUTH"],
)


@auth_dev_router.post(
    "/seed-fake-users",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("admin.access"))],
)
async def seed_users_endpoint(
    session: AsyncSession = Depends(db_manager.get_async_session),
):
    created = await seed_users(session)
    return {
        "status": "ok",
        "created_users": created,
        "default_password": "password123",
    }
