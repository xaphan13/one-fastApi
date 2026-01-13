from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from .models import Base

# Типизация
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Базовый репозиторий с типичными операциями.
    В современном подходе стараются избегать 'God Object' репозиториев,
    но базовый класс для CRUD все же удобен.

    Важное отличие:
    Мы НЕ делаем commit() внутри методов. Транзакциями должен управлять Service layer или UnitOfWork.
    Это позволяет объединять несколько операций в одну транзакцию.
    """

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: Any) -> Optional[ModelType]:
        """Получить одну запись по ID"""
        # SQLAlchemy 2.0 style: select(Model).where(...)
        stmt = select(self.model).where(self.model.id == id) # Предполагается, что у модели есть поле id
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Получить список записей с пагинацией"""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, schema: CreateSchemaType) -> ModelType:
        """Создать запись"""
        # model_dump() - это метод Pydantic v2 (в v1 был dict())
        data = schema.model_dump(exclude_unset=True)
        instance = self.model(**data)
        self.session.add(instance)
        # Мы не делаем commit здесь, только flush если нужно получить ID сразу,
        # но лучше оставить управление транзакцией вызывающему коду.
        return instance

    async def update(
        self,
        instance: ModelType,
        schema: UpdateSchemaType,
        partial: bool = True,
    ) -> ModelType:
        """Обновить запись"""
        data = schema.model_dump(exclude_unset=partial)
        for key, value in data.items():
            setattr(instance, key, value)

        self.session.add(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        """Удалить запись"""
        await self.session.delete(instance)
