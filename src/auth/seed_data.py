from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.rbac.models import Role
from src.auth.security import hash_password

fake = Faker()

PASSWORD = "password123"

USERS_PER_ROLE = {
    "student": 20,
    "teacher": 5,
    "moderator": 2,
    "admin": 1,
}


async def seed_users(session: AsyncSession) -> int:
    result = await session.execute(
        select(Role).where(Role.name.in_(USERS_PER_ROLE.keys()))
    )
    roles = {role.name: role for role in result.scalars().all()}

    missing = set(USERS_PER_ROLE) - set(roles)
    if missing:
        raise RuntimeError(f"❌ Роли не найдены в БД: {missing}")

    created = 0

    for role_name, count in USERS_PER_ROLE.items():
        role = roles[role_name]

        for _ in range(count):
            user = User(
                email=fake.unique.email(),
                name=fake.first_name(),
                surname=fake.last_name(),
                patronymic=fake.first_name(),
                hashed_password=hash_password(PASSWORD),
                is_active=True,
                is_verified=True,
                is_superuser=(role_name == "admin"),
            )

            user.roles.append(role)

            session.add(user)
            created += 1

    await session.commit()
    return created
