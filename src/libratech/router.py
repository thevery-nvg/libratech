from .factory import create_crud_router
from .models import Article, Video, Course
from fastapi import APIRouter
from .schemas import *


article_router = create_crud_router(
    model=Article,
    create_schema=ArticleCreate,
    update_schema=ArticleUpdate,
    read_schema=ArticleRead,
    list_schema=ArticleListRead,
    prefix="/articles",
    tags=["Articles"],
    permissions={
        "read": "book.read",
        "create": "book.create",
        "update": "book.update",
        "delete": "book.delete",
    },
)


video_router = create_crud_router(
    model=Video,
    create_schema=VideoCreate,
    update_schema=VideoUpdate,
    read_schema=VideoRead,
    list_schema=VideoListRead,
    prefix="/videos",
    tags=["Videos"],
    permissions={
        "read": "video.read",
        "create": "video.create",
        "update": "video.update",
        "delete": "video.delete",
    },
)

course_router = create_crud_router(
    model=Course,
    create_schema=CourseCreate,
    update_schema=CourseUpdate,
    read_schema=CourseRead,
    list_schema=CourseListRead,
    prefix="/courses",
    tags=["Courses"],
    permissions={
        "read": "course.read",
        "create": "course.create",
        "update": "course.update",
        "delete": "course.delete",
    },
)

libra_router = APIRouter(prefix="/libra")

libra_router.include_router(article_router)
libra_router.include_router(video_router)
libra_router.include_router(course_router)



