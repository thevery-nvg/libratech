from pydantic import BaseModel
from typing import Optional


class ContentBase(BaseModel):
    title: str
    content: Optional[str] = None
    slug: Optional[str] = None
    is_published: bool

    class Config:
        from_attributes = True

class ContentBaseReduced(BaseModel):
    title: str
    slug: Optional[str] = None
    is_published: bool

    class Config:
        from_attributes = True


# ---------- ARTICLES ----------
class ArticleRead(ContentBase):
    pass


class ArticleListRead(ContentBaseReduced):
    pass


class ArticleCreate(BaseModel):
    title: str
    content: str


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# ---------- VIDEOS ----------

class VideoRead(ContentBase):
    pass


class VideoListRead(ContentBaseReduced):
    pass


class VideoCreate(BaseModel):
    title: str
    # slug: str
    content: Optional[str] = None


class VideoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# ---------- COURSES ----------

class CourseRead(ContentBase):
    pass


class CourseListRead(ContentBaseReduced):
    pass


class CourseCreate(BaseModel):
    title: str
    content: Optional[str] = None


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
