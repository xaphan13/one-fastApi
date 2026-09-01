from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from gem_crud_best.schemas import PostRead, PostCreate
from gem_crud_best.crud import post as crud_post
from gem_crud_best.crud import user as crud_user
from gem_crud_best.core.db_helper import db_helper

router = APIRouter(tags=["Posts"])

@router.get("/", response_model=List[PostRead])
async def get_posts(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    skip: int = 0,
    limit: int = 100,
):
    return await crud_post.get_posts(session, skip=skip, limit=limit)

@router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    post_in: PostCreate,
    user_id: int,
):
    user = await crud_user.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return await crud_post.create_post(session, post_in, user_id)

@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    post_id: int,
):
    post = await crud_post.get_post(session, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post
