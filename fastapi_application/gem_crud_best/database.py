from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy import NullPool

# В продакшене лучше использовать alembic для миграций и config для URL
# sqlite+aiosqlite:///./test.db
DATABASE_URL = "sqlite+aiosqlite:///.app22/test_fast_api.db"

# 1. Настройка движка
# poolclass=NullPool часто используется для SQLite, чтобы избежать проблем с блокировками
# В Postgres production обычно используются настройки пула по умолчанию или оптимизированные
engine = create_async_engine(
    DATABASE_URL,
    echo=True, # Логирование SQL запросов, удобно для отладки
    # future=True, # В 2.0+ это по умолчанию, можно убрать
    poolclass=NullPool
)

# 2. Фабрика сессий
# expire_on_commit=False обязателен для асинхронной работы,
# чтобы объекты оставались доступными после коммита (не требовали повторной загрузки из БД)
async_session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

# 3. Dependency Injection (Зависимость для FastAPI)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессии для внедрения зависимостей в FastAPI.
    Гарантирует закрытие сессии после завершения запроса.
    """
    async with async_session_factory() as session:
        yield session
