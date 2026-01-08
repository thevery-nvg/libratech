from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.manager import db_manager
from src.auth.models import User
from src.rbac.dependencies import require_permission
from src.rbac.permissions import *
from src.rbac.seed_data import seed_rbac

rbac_dev_router = APIRouter(
    prefix="/dev_rbac",
    tags=["DEV_RBAC"],
)


@rbac_dev_router.post(
    "/seed-roles-permissions",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission(DEV))],

)
async def seed_rbac_endpoint(
        session: AsyncSession = Depends(db_manager.get_async_session),
):
    await seed_rbac(session)

    return {"status": "RBAC seeded successfully"}


