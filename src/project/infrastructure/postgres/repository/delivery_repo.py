from typing import Type
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import DeliveryCreate, DeliverySchema
from project.infrastructure.postgres.models import Delivery
from project.core.exceptions import DeliveryNotFound, DeliveryAlreadyExists



class DeliveryRepository:
    _collection: Type[Delivery] = Delivery

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_deliveries(
        self,
        session: AsyncSession,
    ) -> list[DeliverySchema]:
        query = select(self._collection)

        deliveries = await session.scalars(query)

        return [DeliverySchema.model_validate(obj=delivery) for delivery in deliveries.all()]

    async def get_delivery_by_id(
        self,
        session: AsyncSession,
        delivery_id: int,
    ) -> DeliverySchema:
        query = (
            select(self._collection)
            .where(self._collection.deliveryid == delivery_id)
        )

        delivery = await session.scalar(query)

        if not delivery:
            raise DeliveryNotFound(_id=delivery_id)

        return DeliverySchema.model_validate(obj=delivery)

    async def create_delivery(
        self,
        session: AsyncSession,
        delivery: DeliveryCreate,
    ) -> DeliverySchema:
        query = (
            insert(self._collection)
            .values(delivery.model_dump())
            .returning(self._collection)
        )

        try:
            created_delivery = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise DeliveryAlreadyExists(
                supplier_id=delivery.deliveryid,
                date=delivery.datedelivery.strftime("%Y-%m-%d")
            )

        return DeliverySchema.model_validate(obj=created_delivery)

    async def update_delivery(
        self,
        session: AsyncSession,
        delivery_id: int,
        delivery: DeliveryCreate,
    ) -> DeliverySchema:
        query = (
            update(self._collection)
            .where(self._collection.deliveryid == delivery_id)
            .values(delivery.model_dump())
            .returning(self._collection)
        )

        updated_delivery = await session.scalar(query)

        if not updated_delivery:
            raise DeliveryNotFound(_id=delivery_id)

        return DeliverySchema.model_validate(obj=updated_delivery)

    async def delete_delivery(
        self,
        session: AsyncSession,
        delivery_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.deliveryid == delivery_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise DeliveryNotFound(_id=delivery_id)

    async def get_deliveries_by_date(
        self,
        session: AsyncSession,
        delivery_date: date,
    ) -> list[DeliverySchema]:
        query = (
            select(self._collection)
            .where(self._collection.datedelivery == delivery_date)
        )

        deliveries = await session.scalars(query)

        return [DeliverySchema.model_validate(obj=delivery) for delivery in deliveries.all()]
