from fastapi import APIRouter, Depends
from datetime import datetime
import platform
import sys

from src.rbac.dependencies import require_permission

core_router = APIRouter(prefix="/core", tags=["Core"])


@core_router.get("/ping",
                 dependencies=[Depends(require_permission("admin.access"))],
                 )
async def ping():
    return {"status": "ok"}


@core_router.get("/health",
                 dependencies=[Depends(require_permission("admin.access"))],
                 )
async def healthcheck():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@core_router.get("/version",
                 dependencies=[Depends(require_permission("admin.access"))],
                 )
async def version():
    return {
        "python": sys.version,
        "platform": platform.platform(),
    }
