from typing import Type, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from slugify import slugify

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)

async def create_entity(
    session: AsyncSession,
    model: Type[ModelType],
    data,
) -> ModelType:
    entity = model(**data.model_dump())
    session.add(entity)
    await session.commit()
    await session.refresh(entity)
    return entity


async def get_by_slug(
    session: AsyncSession,
    model: Type[ModelType],
    slug: str,
) -> ModelType | None:
    result = await session.execute(
        select(model).where(model.slug == slug)
    )
    return result.scalar_one_or_none()


async def update_by_slug(
    session: AsyncSession,
    model: Type[ModelType],
    slug: str,
    data,
) -> ModelType | None:
    entity = await get_by_slug(session, model, slug)

    if not entity:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(entity, field, value)

    await session.commit()
    await session.refresh(entity)
    return entity


async def delete_by_slug(
    session: AsyncSession,
    model: Type[ModelType],
    slug: str,
) -> bool:
    entity = await get_by_slug(session, model, slug)

    if not entity:
        return False

    await session.delete(entity)
    await session.commit()
    return True

async def list_entities(
    session: AsyncSession,
    model: Type,
    *,
    is_published: bool = False,
):
    stmt = select(model)

    if is_published and hasattr(model, "is_published"):
        stmt = stmt.where(model.is_published.is_(True))

    result = await session.execute(stmt)
    return result.scalars().all()


async def seed_entities(
    session: AsyncSession,
    entities: list,
):
    session.add_all(entities)
    await session.commit()