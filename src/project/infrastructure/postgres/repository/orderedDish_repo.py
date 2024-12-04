from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, and_
from sqlalchemy.exc import IntegrityError


from project.schemas.user import OrderedDishCreate, OrderedDishSchema
from project.infrastructure.postgres.models import OrderedDish
from project.core.exceptions import OrderedDishNotFound, OrderedDishAlreadyExists



class OrderedDishRepository:
    _collection: Type[OrderedDish] = OrderedDish

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_ordered_dishes(
        self,
        session: AsyncSession,
    ) -> list[OrderedDishSchema]:
        query = select(self._collection)

        ordered_dishes = await session.scalars(query)

        return [OrderedDishSchema.model_validate(obj=dish) for dish in ordered_dishes.all()]

    async def get_ordered_dish(
        self,
        session: AsyncSession,
        order_id: int,
        dish_id: int,
    ) -> OrderedDishSchema:
        query = (
            select(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.dishid == dish_id
                )
            )
        )

        ordered_dish = await session.scalar(query)

        if not ordered_dish:
            raise OrderedDishNotFound(dish_id=dish_id, order_id=order_id)

        return OrderedDishSchema.model_validate(obj=ordered_dish)

    async def get_dishes_by_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> list[OrderedDishSchema]:
        query = (
            select(self._collection)
            .where(self._collection.orderid == order_id)
        )

        ordered_dishes = await session.scalars(query)

        return [OrderedDishSchema.model_validate(obj=dish) for dish in ordered_dishes.all()]

    async def create_ordered_dish(
        self,
        session: AsyncSession,
        ordered_dish: OrderedDishCreate,
    ) -> OrderedDishSchema:
        query = (
            insert(self._collection)
            .values(ordered_dish.model_dump())
            .returning(self._collection)
        )

        try:
            created_ordered_dish = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise OrderedDishAlreadyExists(
                dish_id=ordered_dish.dishid,
                order_id=ordered_dish.orderid
            )

        return OrderedDishSchema.model_validate(obj=created_ordered_dish)

    async def update_ordered_dish(
        self,
        session: AsyncSession,
        order_id: int,
        dish_id: int,
        ordered_dish: OrderedDishCreate,
    ) -> OrderedDishSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.dishid == dish_id
                )
            )
            .values(ordered_dish.model_dump())
            .returning(self._collection)
        )

        updated_ordered_dish = await session.scalar(query)

        if not updated_ordered_dish:
            raise OrderedDishNotFound(dish_id=dish_id, order_id=order_id)

        return OrderedDishSchema.model_validate(obj=updated_ordered_dish)

    async def delete_ordered_dish(
        self,
        session: AsyncSession,
        order_id: int,
        dish_id: int,
    ) -> None:
        query = (
            delete(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.dishid == dish_id
                )
            )
        )

        result = await session.execute(query)

        if not result.rowcount:
            raise OrderedDishNotFound(dish_id=dish_id, order_id=order_id)

    async def update_dish_count(
        self,
        session: AsyncSession,
        order_id: int,
        dish_id: int,count: int,
    ) -> OrderedDishSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.dishid == dish_id
                )
            )
            .values(count=count)
            .returning(self._collection)
        )

        updated_ordered_dish = await session.scalar(query)

        if not updated_ordered_dish:
            raise OrderedDishNotFound(dish_id=dish_id, order_id=order_id)

        return OrderedDishSchema.model_validate(obj=updated_ordered_dish)

    async def delete_dishes_from_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> None:
        query = delete(self._collection).where(self._collection.orderid == order_id)
        await session.execute(query)
