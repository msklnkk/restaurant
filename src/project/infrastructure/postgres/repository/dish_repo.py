from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import DishCreate, DishSchema
from project.infrastructure.postgres.models import Dish
from project.core.exceptions import DishNotFound, DishAlreadyExists


class DishRepository:
    _collection: Type[Dish] = Dish

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_dishes(
        self,
        session: AsyncSession,
    ) -> list[DishSchema]:
        query = select(self._collection)

        dishes = await session.scalars(query)

        return [DishSchema.model_validate(obj=dish) for dish in dishes.all()]

    async def get_dish_by_id(
        self,
        session: AsyncSession,
        dish_id: int,
    ) -> DishSchema:
        query = (
            select(self._collection)
            .where(self._collection.dishid == dish_id)
        )

        dish = await session.scalar(query)

        if not dish:
            raise DishNotFound(_id=dish_id)

        return DishSchema.model_validate(obj=dish)

    async def get_dishes_by_type(
        self,
        session: AsyncSession,
        dish_type: str,
    ) -> list[DishSchema]:
        query = (
            select(self._collection)
            .where(self._collection.type == dish_type)
        )

        dishes = await session.scalars(query)

        return [DishSchema.model_validate(obj=dish) for dish in dishes.all()]

    async def create_dish(
        self,
        session: AsyncSession,
        dish: DishCreate,
    ) -> DishSchema:
        query = (
            insert(self._collection)
            .values(dish.model_dump())
            .returning(self._collection)
        )

        try:
            created_dish = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise DishAlreadyExists(name=dish.name)

        return DishSchema.model_validate(obj=created_dish)

    async def update_dish(
        self,
        session: AsyncSession,
        dish_id: int,
        dish: DishCreate,
    ) -> DishSchema:
        query = (
            update(self._collection)
            .where(self._collection.dishid == dish_id)
            .values(dish.model_dump())
            .returning(self._collection)
        )

        updated_dish = await session.scalar(query)

        if not updated_dish:
            raise DishNotFound(_id=dish_id)

        return DishSchema.model_validate(obj=updated_dish)

    async def delete_dish(
        self,
        session: AsyncSession,
        dish_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.dishid == dish_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise DishNotFound(_id=dish_id)

    async def search_dishes_by_name(
        self,
        session: AsyncSession,
        name: str
    ) -> list[DishSchema]:
        query = (
            select(self._collection)
            .where(self._collection.name.ilike(f"%{name}%"))
        )

        dishes = await session.scalars(query)

        return [DishSchema.model_validate(obj=dish) for dish in dishes.all()]
