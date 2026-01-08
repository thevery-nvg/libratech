from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.manager import db_manager
from src.rbac.dependencies import require_permission
from .service import seed_entities
from .seed_data import generate_videos,generate_articles,generate_courses


dev_router = APIRouter(
    prefix="/dev_content",
    tags=["DEV_CONTENT"],
    dependencies=[Depends(require_permission("content.create"))],
)
@dev_router.post(
    "/seed-content-faker",
    status_code=status.HTTP_201_CREATED,
)
async def seed_content_faker(
    session: AsyncSession = Depends(db_manager.get_async_session),
):
    articles = generate_articles(25)
    videos = generate_videos(25)
    courses = generate_courses(25)

    await seed_entities(session, articles)
    await seed_entities(session, videos)
    await seed_entities(session, courses)

    return {
        "articles": len(articles),
        "videos": len(videos),
        "courses": len(courses),
        "status": "ok",
    }