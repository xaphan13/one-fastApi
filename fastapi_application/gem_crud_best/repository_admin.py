from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .repository_base import BaseRepository
from .models import AdminList, AdminWork
from pydantic import BaseModel

# --- Pydantic Schemas (DTOs) ---
# Обычно лежат в schemas.py, но для примера здесь

class AdminWorkCreate(BaseModel):
    type_work: str
    callback_data: str

class AdminListCreate(BaseModel):
    user_id: str
    # Вложенные данные для создания
    works: Optional[List[AdminWorkCreate]] = None

class AdminListUpdate(BaseModel):
    user_id: Optional[str] = None

# --- Specific Repository ---

class AdminRepository(BaseRepository[AdminList, AdminListCreate, AdminListUpdate]):
    """
    Репозиторий конкретной доменной области.
    Здесь пишутся сложные запросы, специфичные для AdminList.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(AdminList, session)

    async def get_by_user_id(self, user_id: str) -> Optional[AdminList]:
        """
        Пример кастомного метода поиска.
        Используем selectinload для подгрузки связанных данных (Eager Loading).
        """
        stmt = (
            select(AdminList)
            .where(AdminList.user_id == user_id)
            .options(selectinload(AdminList.admin_worked)) # Оптимизированная подгрузка
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_with_works(self, schema: AdminListCreate) -> AdminList:
        """
        Пример сложного создания со связанными сущностями.
        """
        # Создаем родителя
        admin_list = AdminList(user_id=schema.user_id)

        # Если есть вложенные работы, создаем их
        if schema.works:
            for work_data in schema.works:
                work = AdminWork(
                    type_work=work_data.type_work,
                    callback_data=work_data.callback_data
                )
                # SQLAlchemy сам свяжет их через relationship
                admin_list.admin_worked.append(work)

        self.session.add(admin_list)
        return admin_list
