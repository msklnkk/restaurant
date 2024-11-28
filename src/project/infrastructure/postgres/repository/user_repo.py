from typing import Type
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import ClientCreate, ClientSchema, DrinkSchema, DrinkCreate, PriceSchema, PriceCreate
from project.infrastructure.postgres.models import Client, Drink, Price


from project.core.exceptions import UserNotFound, UserAlreadyExists, DrinkNotFound, DrinkAlreadyExists
from project.core.exceptions import PriceNotFound, PriceAlreadyExists

class ClientRepository:
    _collection: Type[Client] = Client

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[ClientSchema]:
        query = select(self._collection)

        users = await session.scalars(query)

        return [ClientSchema.model_validate(obj=user) for user in users.all()]

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> ClientSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == user_id)
        )

        user = await session.scalar(query)

        if not user:
            raise UserNotFound(_id=user_id)

        return ClientSchema.model_validate(obj=user)

    async def create_user(
        self,
        session: AsyncSession,
        user: ClientCreate,
    ) -> ClientSchema:
        query = (
            insert(self._collection)
            .values(user.model_dump())
            .returning(self._collection)
        )

        try:
            created_user = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise UserAlreadyExists(email=user.email)

        return ClientSchema.model_validate(obj=created_user)

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        user: ClientCreate,
    ) -> ClientSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == user_id)
            .values(user.model_dump())
            .returning(self._collection)
        )

        updated_user = await session.scalar(query)

        if not updated_user:
            raise UserNotFound(_id=user_id)

        return ClientSchema.model_validate(obj=updated_user)

    async def delete_user(
        self,
        session: AsyncSession,
        user_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == user_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise UserNotFound(_id=user_id)

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


# Price

class PriceRepository:
    _collection: Type[Price] = Price

    async def check_connection(
        self,
        session: AsyncSession,я
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_prices(
        self,
        session: AsyncSession,
    ) -> list[PriceSchema]:
        query = select(self._collection)

        prices = await session.scalars(query)

        return [PriceSchema.model_validate(obj=price) for price in prices.all()]

    async def get_price_by_id(
        self,
        session: AsyncSession,
        dishid: int,
    ) -> PriceSchema:
        query = (
            select(self._collection)
            .where(self._collection.dishid == dishid)
        )

        price = await session.scalar(query)

        if not price:
            raise PriceNotFound(_id=dishid)

        return PriceSchema.model_validate(obj=price)

    async def create_price(
        self,
        session: AsyncSession,
        price: PriceCreate,
    ) -> PriceSchema:
        query = (
            insert(self._collection)
            .values(price.model_dump(exclude_unset=True))
            .returning(self._collection)
        )

        try:
            created_price = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise PriceAlreadyExists(dish_id=created_price.dishid)

        return PriceSchema.model_validate(obj=created_price)

    async def update_price(
        self,
        session: AsyncSession,
        dishid: int,
        price: PriceCreate,
    ) -> PriceSchema:
        query = (
            update(self._collection)
            .where(self._collection.dishid == dishid)
            .values(price.model_dump(exclude_unset=True))
            .returning(self._collection)
        )

        updated_price = await session.scalar(query)

        if not updated_price:
            raise PriceNotFound(_id=dishid)

        return PriceSchema.model_validate(obj=updated_price)

    async def delete_price(
        self,
        session: AsyncSession,
        dishid: int
    ) -> None:
        query = delete(self._collection).where(self._collection.dishid == dishid)

        result = await session.execute(query)

        if not result.rowcount:
            raise PriceNotFound(_id=dishid)
