from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .database import get_db
from .models import AdminList
from .repository_admin import AdminRepository, AdminListCreate, AdminListUpdate

# Эмуляция Service Layer
class AdminService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = AdminRepository(session)

    async def register_admin(self, schema: AdminListCreate) -> AdminList:
        # Бизнес-логика: проверка существования
        existing = await self.repo.get_by_user_id(schema.user_id)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Admin already exists"
            )

        # Создание
        new_admin = await self.repo.create_with_works(schema)

        # ! ВАЖНО: Коммит происходит на уровне сервиса,
        # когда мы уверены, что вся бизнес-операция прошла успешно.
        await self.session.commit()

        # В асинхронном коде, если мы хотим обратиться к атрибутам (особенно relations)
        # после коммита (когда сессия закрыла транзакцию), нам нужно быть осторожными.
        # expire_on_commit=False в настройках сессии помогает,
        # но для relations нужно убедиться, что они загружены.

        # Лучший способ - сделать рефреш с явной подгрузкой
        # Или просто вернуть объект, если мы знаем, что relations нам не нужны для ответа API
        # или если мы использовали lazy='selectin' в модели (но лучше explicit load)

        # В данном примере, так как мы только что создали объекты, они есть в Identity Map.
        # Но если мы хотим вернуть полный граф объектов, лучше вернуть то, что мы создали,
        # так как мы сами его наполнили данными.

        return new_admin

    async def get_admin_info(self, user_id: str):
        admin = await self.repo.get_by_user_id(user_id)
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        return admin
