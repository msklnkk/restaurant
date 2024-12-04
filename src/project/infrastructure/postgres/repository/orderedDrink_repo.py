from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, and_
from sqlalchemy.exc import IntegrityError

from project.schemas.user import OrderedDrinkCreate, OrderedDrinkSchema
from project.infrastructure.postgres.models import OrderedDrink
from project.core.exceptions import OrderedDrinkNotFound, OrderedDrinkAlreadyExists


class OrderedDrinkRepository:
    _collection: Type[OrderedDrink] = OrderedDrink

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_ordered_drinks(
        self,
        session: AsyncSession,
    ) -> list[OrderedDrinkSchema]:
        query = select(self._collection)

        ordered_drinks = await session.scalars(query)

        return [OrderedDrinkSchema.model_validate(obj=drink) for drink in ordered_drinks.all()]

    async def get_ordered_drink(
        self,
        session: AsyncSession,
        order_id: int,
        drink_id: int,
    ) -> OrderedDrinkSchema:
        query = (
            select(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.drinkid == drink_id
                )
            )
        )

        ordered_drink = await session.scalar(query)

        if not ordered_drink:
            raise OrderedDrinkNotFound(drink_id=drink_id, order_id=order_id)

        return OrderedDrinkSchema.model_validate(obj=ordered_drink)

    async def get_drinks_by_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> list[OrderedDrinkSchema]:
        query = (
            select(self._collection)
            .where(self._collection.orderid == order_id)
        )

        ordered_drinks = await session.scalars(query)

        return [OrderedDrinkSchema.model_validate(obj=drink) for drink in ordered_drinks.all()]

    async def create_ordered_drink(
        self,
        session: AsyncSession,
        ordered_drink: OrderedDrinkCreate,
    ) -> OrderedDrinkSchema:
        query = (
            insert(self._collection)
            .values(ordered_drink.model_dump())
            .returning(self._collection)
        )

        try:
            created_ordered_drink = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise OrderedDrinkAlreadyExists(
                drink_id=ordered_drink.drinkid,
                order_id=ordered_drink.orderid
            )

        return OrderedDrinkSchema.model_validate(obj=created_ordered_drink)

    async def update_ordered_drink(
        self,
        session: AsyncSession,
        order_id: int,
        drink_id: int,
        ordered_drink: OrderedDrinkCreate,
    ) -> OrderedDrinkSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.drinkid == drink_id
                )
            )
            .values(ordered_drink.model_dump())
            .returning(self._collection)
        )

        updated_ordered_drink = await session.scalar(query)

        if not updated_ordered_drink:
            raise OrderedDrinkNotFound(drink_id=drink_id, order_id=order_id)

        return OrderedDrinkSchema.model_validate(obj=updated_ordered_drink)

    async def delete_ordered_drink(
        self,
        session: AsyncSession,
        order_id: int,
        drink_id: int,
    ) -> None:
        query = (
            delete(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.drinkid == drink_id
                )
            )
        )

        result = await session.execute(query)

        if not result.rowcount:
            raise OrderedDrinkNotFound(drink_id=drink_id, order_id=order_id)

    async def update_drink_count(
        self,
        session:AsyncSession,
        order_id: int,
        drink_id: int,
        count: int,
    ) -> OrderedDrinkSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.drinkid == drink_id
                )
            )
            .values(count=count)
            .returning(self._collection)
        )

        updated_ordered_drink = await session.scalar(query)

        if not updated_ordered_drink:
            raise OrderedDrinkNotFound(drink_id=drink_id, order_id=order_id)

        return OrderedDrinkSchema.model_validate(obj=updated_ordered_drink)

    async def delete_drinks_from_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> None:
        query = delete(self._collection).where(self._collection.orderid == order_id)
        await session.execute(query)