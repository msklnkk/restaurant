from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError


from project.schemas.user import DrinkSchema, DrinkCreate
from project.infrastructure.postgres.models import Drink
from project.core.exceptions import DrinkNotFound, DrinkAlreadyExists

class DrinkRepository:
    _collection: Type[Drink] = Drink

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_drinks(
        self,
        session: AsyncSession,
    ) -> list[DrinkSchema]:
        query = select(self._collection)

        drinks = await session.scalars(query)

        return [DrinkSchema.model_validate(obj=drink) for drink in drinks.all()]

    async def get_drink_by_id(
        self,
        session: AsyncSession,
        drink_id: int,
    ) -> DrinkSchema:
        query = (
            select(self._collection)
            .where(self._collection.drinkid == drink_id)
        )

        drink = await session.scalar(query)

        if not drink:
            raise DrinkNotFound(_id=drink_id)

        return DrinkSchema.model_validate(obj=drink)

    async def create_drink(
        self,
        session: AsyncSession,
        drink: DrinkCreate,
    ) -> DrinkSchema:
        query = (
            insert(self._collection)
            .values(drink.model_dump(exclude_unset=True))
            .returning(self._collection)
        )

        try:
            created_drink = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise DrinkAlreadyExists(name=drink.name)

        return DrinkSchema.model_validate(obj=created_drink)

    async def update_drink(
        self,
        session: AsyncSession,
        drink_id: int,
        drink: DrinkCreate,
    ) -> DrinkSchema:
        query = (
            update(self._collection)
            .where(self._collection.drinkid == drink_id)
            .values(drink.model_dump(exclude_unset=True))
            .returning(self._collection)
        )

        updated_drink = await session.scalar(query)

        if not updated_drink:
            raise DrinkNotFound(_id=drink_id)

        return DrinkSchema.model_validate(obj=updated_drink)

    async def delete_drink(
        self,
        session: AsyncSession,
        drink_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.drinkid == drink_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise DrinkNotFound(_id=drink_id)
