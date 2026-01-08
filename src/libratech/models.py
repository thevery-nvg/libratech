from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import String, Text,Boolean
from src.core.db.base import Base
from slugify import slugify
import uuid


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    @validates("title")
    def generate_slug(self, key, value):
        if not self.slug:
            self.slug = f"{slugify(value)}-{uuid.uuid4().hex[:8]}"
        return value


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    @validates("title")
    def generate_slug(self, key, value):
        if not self.slug:
            self.slug = f"{slugify(value)}-{uuid.uuid4().hex[:8]}"
        return value


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    @validates("title")
    def generate_slug(self, key, value):
        if not self.slug:
            self.slug = f"{slugify(value)}-{uuid.uuid4().hex[:8]}"
        return value
