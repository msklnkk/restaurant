from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import PriceSchema, PriceCreate
from project.infrastructure.postgres.models import Price
from project.core.exceptions import PriceNotFound, PriceAlreadyExists

class PriceRepository:
    _collection: Type[Price] = Price

    async def check_connection(
        self,
        session: AsyncSession,
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
