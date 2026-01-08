from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate, UserUpdate
from .security import hash_password, verify_password
from ..rbac.models import Role


async def get_user_by_email(
        session: AsyncSession,
        email: str,
) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(
        session: AsyncSession,
        user_id: int,
) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def register_user(
        session: AsyncSession,
        data: UserCreate,
) -> User:
    existing_user = await get_user_by_email(session, str(data.email))
    if existing_user:
        raise ValueError("Пользователь с таким email уже существует")

    if data.password != data.password_repeat:
        raise ValueError("Пароли не совпадают")

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        name=data.name,
        surname=data.surname,
        patronymic=data.patronymic,
        is_active=True,
        is_superuser=False,
        is_verified=False,
    )
    student_role = await session.scalar(
        select(Role).where(Role.name == "student")
    )
    if not student_role:
        raise RuntimeError(
            "Default role 'student' not found. Seed RBAC first."
        )

    user.roles.append(student_role)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def authenticate_user(
        session: AsyncSession,
        email: str,
        password: str,
) -> Optional[User]:
    user = await get_user_by_email(session, email)
    if not user:
        return None

    if not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


async def update_user(
        session: AsyncSession,
        user: User,
        data: UserUpdate,
) -> User:
    update_data = data.model_dump(exclude_unset=True)

    if 'password' in update_data:
        update_data['hashed_password'] = hash_password(update_data.pop('password'))

    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)
        elif hasattr(user, f'{field}_id'):  # для внешних ключей
            setattr(user, f'{field}_id', value)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def deactivate_user(
        session: AsyncSession,
        user: User,
) -> None:
    user.is_active = False

    session.add(user)
    await session.commit()
