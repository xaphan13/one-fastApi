from fastapi import APIRouter
from .users import router as users_router
from .posts import router as posts_router

router = APIRouter()
router.include_router(users_router, prefix="/users")
router.include_router(posts_router, prefix="/posts")
