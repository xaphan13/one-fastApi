from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from gem_crud_best.models import User
from gem_crud_best.schemas import UserCreate, UserUpdate

async def get_users(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> Sequence[User]:
    stmt = select(User).offset(skip).limit(limit).order_by(User.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)

async def get_user_by_nickname(session: AsyncSession, nickname: str) -> User | None:
    stmt = select(User).where(User.nickname == nickname)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    # TODO: Hash the password before saving!
    # For example: user_in.password = get_password_hash(user_in.password)
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate,
    partial: bool = True,
) -> User:
    for name, value in user_update.model_dump(exclude_unset=partial).items():
        setattr(user, name, value)
    await session.commit()
    await session.refresh(user)
    return user

async def delete_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()
