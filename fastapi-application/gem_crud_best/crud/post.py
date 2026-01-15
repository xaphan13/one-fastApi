from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from gem_crud_best.models import Post
from gem_crud_best.schemas import PostCreate

async def get_posts(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100
) -> Sequence[Post]:
    stmt = select(Post).offset(skip).limit(limit).order_by(Post.id)
    result = await session.execute(stmt)
    return result.scalars().all()

async def create_post(
    session: AsyncSession,
    post_in: PostCreate,
    user_id: int
) -> Post:
    post = Post(**post_in.model_dump(), user_id=user_id)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

async def get_post(session: AsyncSession, post_id: int) -> Post | None:
    return await session.get(Post, post_id)

async def delete_post(session: AsyncSession, post: Post) -> None:
    await session.delete(post)
    await session.commit()
