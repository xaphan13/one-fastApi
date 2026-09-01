from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gem_crud_best.core.base import Base
from .types import intpk, created_at, str50

if TYPE_CHECKING:
    from .user import User

class Post(Base):
    id: Mapped[intpk]
    time_created: Mapped[created_at]
    title: Mapped[str50]
    content: Mapped[str] = mapped_column(Text)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    author: Mapped["User"] = relationship(back_populates="posts")
