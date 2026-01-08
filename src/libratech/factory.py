from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.manager import db_manager
from src.rbac.dependencies import require_permission
from . import service


def create_crud_router(
        *,
        model,
        create_schema,
        update_schema,
        read_schema,
        list_schema,
        prefix: str,
        tags: list[str],
        permissions: dict,
        is_published: bool = True,
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    @router.post(
        "",
        response_model=read_schema,
        dependencies=[Depends(require_permission(permissions["create"]))],
    )
    async def create(
            data: create_schema,
            session: AsyncSession = Depends(db_manager.get_async_session),
    ):
        return await service.create_entity(session, model, data)

    @router.get(
        "/{slug}",
        response_model=read_schema,
        dependencies=[Depends(require_permission(permissions["read"]))],
    )
    async def get(slug: str, session: AsyncSession = Depends(db_manager.get_async_session)):
        entity = await service.get_by_slug(session, model, slug)
        if not entity:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return entity

    @router.patch(
        "/{slug}",
        response_model=read_schema,
        dependencies=[Depends(require_permission(permissions["update"]))],
    )
    async def update(
            slug: str,
            data: update_schema,
            session: AsyncSession = Depends(db_manager.get_async_session),
    ):
        entity = await service.update_by_slug(session, model, slug, data)
        if not entity:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        return entity

    @router.delete(
        "/{slug}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Depends(require_permission(permissions["delete"]))],
    )
    async def delete(
            slug: str,
            session: AsyncSession = Depends(db_manager.get_async_session),
    ):
        ok = await service.delete_by_slug(session, model, slug)
        if not ok:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

    @router.get(
        "",
        response_model=list[list_schema],
    )
    async def list_items(
        session: AsyncSession = Depends(db_manager.get_async_session),
    ):
        return await service.list_entities(session, model, is_published=is_published)

    return router



