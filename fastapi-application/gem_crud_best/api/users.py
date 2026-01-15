from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from gem_crud_best.schemas import UserRead, UserCreate
from gem_crud_best.crud import user as crud_user
from gem_crud_best.core.db_helper import db_helper

router = APIRouter(tags=["Users"])

@router.get("/", response_model=List[UserRead])
async def get_users(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    skip: int = 0,
    limit: int = 100,
):
    return await crud_user.get_users(session, skip=skip, limit=limit)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_in: UserCreate,
):
    return await crud_user.create_user(session, user_in)

@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    user_id: int,
):
    user = await crud_user.get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
