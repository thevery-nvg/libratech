from faker import Faker
from typing import Type
from sqlalchemy.orm import DeclarativeBase

from src.libratech.models import Article, Video, Course

faker = Faker("en_US")


def fake_title() -> str:
    return faker.sentence(nb_words=8)


def fake_content() -> str:
    return "\n\n".join(faker.paragraphs(nb=5))

def generate_entities(
    model: Type[DeclarativeBase],
    count: int,
    *,
    is_published: bool,
):
    entities = []

    for _ in range(count):
        entities.append(
            model(
                title=fake_title(),
                content=fake_content(),
                is_published=is_published,
            )
        )

    return entities
def generate_articles(count: int = 10):
    return generate_entities(Article, count, is_published=True)


def generate_videos(count: int = 10):
    return generate_entities(Video, count, is_published=True)


def generate_courses(count: int = 10):
    return generate_entities(Course, count, is_published=True)

if __name__ == '__main__':
    print(fake_title())
