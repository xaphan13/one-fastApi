from typing import TYPE_CHECKING, List
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from gem_crud_best.core.base import Base
from .types import intpk, str20, str50

if TYPE_CHECKING:
    from .post import Post

class User(Base):
    id: Mapped[intpk]
    nickname: Mapped[str20] = mapped_column(unique=True)
    firstname: Mapped[str20 | None]
    surname: Mapped[str20 | None]
    password: Mapped[str50 | None]

    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("firstname", "surname"),)
