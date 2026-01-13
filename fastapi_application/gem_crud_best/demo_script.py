import asyncio
import sys
import os

# Добавляем корневую директорию в путь, чтобы импорты работали
sys.path.append(os.getcwd())

from fastapi_application.gem_crud_best.database import engine, get_db, async_session_factory
from fastapi_application.gem_crud_best.models import Base, AdminList, AdminWork
from fastapi_application.gem_crud_best.service import AdminService
from fastapi_application.gem_crud_best.repository_admin import AdminListCreate, AdminWorkCreate

async def init_models():
    """Создаем таблицы в базе данных"""
    async with engine.begin() as conn:
        # В продакшене используйте Alembic!
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")

async def main():
    # 1. Инициализация БД
    await init_models()

    # 2. Эмуляция работы в рамках запроса (получение сессии)
    async with async_session_factory() as session:
        service = AdminService(session)

        # 3. Тест создания
        print("\n--- Creating Admin ---")
        new_admin_data = AdminListCreate(
            user_id="user_123",
            works=[
                AdminWorkCreate(type_work="setup", callback_data="btn_setup"),
                AdminWorkCreate(type_work="monitor", callback_data="btn_monitor"),
            ]
        )

        try:
            admin = await service.register_admin(new_admin_data)
            print(f"Created Admin: {admin}")
            print(f"Works count: {len(admin.admin_worked)}")
            for w in admin.admin_worked:
                print(f" - Work: {w.type_work}")
        except Exception as e:
            print(f"Error creating admin: {e}")

        # 4. Тест получения (с подгрузкой отношений)
        print("\n--- Fetching Admin ---")
        fetched_admin = await service.get_admin_info("user_123")
        print(f"Fetched: {fetched_admin}")
        print(f"Fetched Works: {len(fetched_admin.admin_worked)}")

    # Завершение работы движка
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
