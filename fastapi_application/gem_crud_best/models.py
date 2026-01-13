from __future__ import annotations
from typing import Annotated, List, Optional
from datetime import datetime, timezone

from sqlalchemy import String, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Custom Types (Аннотации типов для повторного использования)
# Использование intpk делает код чище и понятнее
intpk = Annotated[int, mapped_column(primary_key=True, index=True)]

# Datetime с таймзоной (Best Practice: всегда хранить время в UTC)
created_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
]

updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=datetime.now(timezone.utc)
    )
]

# --- Примеры моделей ---

class AdminList(Base):
    __tablename__ = "admin_list"

    # Использование 'id' как стандартное имя PK упрощает Generic Repository
    id: Mapped[intpk]

    user_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Отношения также типизированы
    # cascade="all, delete-orphan" удаляет связанные записи при удалении родителя
    admin_worked: Mapped[List["AdminWork"]] = relationship(
        back_populates="admin_list",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<AdminList(id={self.id}, user_id='{self.user_id}')>"


class AdminWork(Base):
    __tablename__ = "admin_work"

    id: Mapped[intpk]

    type_work: Mapped[str] = mapped_column(String)
    callback_data: Mapped[str] = mapped_column(String)

    # ForeignKey указывает на таблицу и колонку
    # Обратите внимание: admin_list.id (так как мы переименовали PK в id)
    admin_id: Mapped[int] = mapped_column(
        ForeignKey("admin_list.id", ondelete="CASCADE")
    )

    # Обратная связь
    admin_list: Mapped["AdminList"] = relationship(back_populates="admin_worked")

    def __repr__(self):
        return f"<AdminWork(id={self.id}, type='{self.type_work}')>"


# Примеры из старого кода, переписанные в новом стиле
class Person(Base):
    __tablename__ = "persons"

    id: Mapped[intpk]
    created_at: Mapped[created_at]

    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    # Optional[int] означает что колонка может быть NULL (nullable=True по умолчанию в Mapped[Optional])
    link_addr_id: Mapped[Optional[int]] = mapped_column(ForeignKey("addresses.id"), nullable=True)

    address: Mapped[Optional["Address"]] = relationship(back_populates="persons")


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[intpk]
    created_at: Mapped[created_at]

    city: Mapped[str] = mapped_column(String(50))
    street: Mapped[str] = mapped_column(String(100))
    addr_index: Mapped[int] = mapped_column(default=0)

    persons: Mapped[List["Person"]] = relationship(back_populates="address")
