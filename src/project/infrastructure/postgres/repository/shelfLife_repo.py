from typing import Type
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, and_
from sqlalchemy.exc import IntegrityError

from project.schemas.user import ShelfLifeCreate, ShelfLifeSchema
from project.infrastructure.postgres.models import ShelfLife
from project.core.exceptions import ShelfLifeNotFound, ShelfLifeAlreadyExists



class ShelfLifeRepository:
    _collection: Type[ShelfLife] = ShelfLife

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_shelf_lives(
        self,
        session: AsyncSession,
    ) -> list[ShelfLifeSchema]:
        query = select(self._collection)

        shelf_lives = await session.scalars(query)

        return [ShelfLifeSchema.model_validate(obj=shelf_life) for shelf_life in shelf_lives.all()]

    async def get_shelf_life(
        self,
        session: AsyncSession,
        shelf_id: int,
        delivery_id: int,
    ) -> ShelfLifeSchema:
        query = (
            select(self._collection)
            .where(
                and_(
                    self._collection.shelflifeid == shelf_id,
                    self._collection.deliveryID == delivery_id
                )
            )
        )

        shelf_life = await session.scalar(query)

        if not shelf_life:
            raise ShelfLifeNotFound(shelf_id=shelf_id, delivery_id=delivery_id)

        return ShelfLifeSchema.model_validate(obj=shelf_life)

    async def get_shelf_lives_by_delivery(
        self,
        session: AsyncSession,
        delivery_id: int,
    ) -> list[ShelfLifeSchema]:
        query = (
            select(self._collection)
            .where(self._collection.deliveryID == delivery_id)
        )

        shelf_lives = await session.scalars(query)

        return [ShelfLifeSchema.model_validate(obj=shelf_life) for shelf_life in shelf_lives.all()]

    async def create_shelf_life(
        self,
        session: AsyncSession,
        shelf_life: ShelfLifeCreate,
    ) -> ShelfLifeSchema:
        query = (
            insert(self._collection)
            .values(shelf_life.model_dump())
            .returning(self._collection)
        )

        try:
            created_shelf_life = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise ShelfLifeAlreadyExists(
                shelf_id=shelf_life.shelflifeid,
                delivery_id=shelf_life.deliveryID
            )

        return ShelfLifeSchema.model_validate(obj=created_shelf_life)

    async def update_shelf_life(
        self,
        session: AsyncSession,
        shelf_id: int,
        delivery_id: int,
        shelf_life: ShelfLifeCreate,
    ) -> ShelfLifeSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.shelflifeid == shelf_id,
                    self._collection.deliveryID == delivery_id
                )
            )
            .values(shelf_life.model_dump())
            .returning(self._collection)
        )

        updated_shelf_life = await session.scalar(query)

        if not updated_shelf_life:
            raise ShelfLifeNotFound(shelf_id=shelf_id, delivery_id=delivery_id)

        return ShelfLifeSchema.model_validate(obj=updated_shelf_life)

    async def delete_shelf_life(
        self,
        session: AsyncSession,
        shelf_id: int,
        delivery_id: int,
    ) -> None:
        query = (
            delete(self._collection)
            .where(
                and_(
                    self._collection.shelflifeid == shelf_id,
                    self._collection.deliveryID == delivery_id
                )
            )
        )

        result = await session.execute(query)

        if not result.rowcount:
            raise ShelfLifeNotFound(shelf_id=shelf_id, delivery_id=delivery_id)

    async def get_expired_shelf_lives(
        self,session: AsyncSession,
        current_date: date = None,
    ) -> list[ShelfLifeSchema]:
        if current_date is None:
            current_date = date.today()

        query = (
            select(self._collection)
            .where(self._collection.expirationdate < current_date)
        )

        expired_items = await session.scalars(query)

        return [ShelfLifeSchema.model_validate(obj=item) for item in expired_items.all()]

    async def delete_shelf_lives_by_delivery(
        self,
        session: AsyncSession,
        delivery_id: int,
    ) -> None:
        query = delete(self._collection).where(self._collection.deliveryID == delivery_id)
        await session.execute(query)
