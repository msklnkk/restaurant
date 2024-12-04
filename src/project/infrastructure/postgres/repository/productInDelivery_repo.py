from typing import Type
from decimal import Decimal
from sqlalchemy import func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, and_
from sqlalchemy.exc import IntegrityError

from project.schemas.user import ProductInDeliveryCreate, ProductInDeliverySchema
from project.infrastructure.postgres.models import ProductInDelivery
from project.core.exceptions import ProductInDeliveryNotFound, ProductInDeliveryAlreadyExists



class ProductInDeliveryRepository:
    _collection: Type[ProductInDelivery] = ProductInDelivery

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_products_in_deliveries(
        self,
        session: AsyncSession,
    ) -> list[ProductInDeliverySchema]:
        query = select(self._collection)

        products = await session.scalars(query)

        return [ProductInDeliverySchema.model_validate(obj=product) for product in products.all()]

    async def get_product_in_delivery(
        self,
        session: AsyncSession,
        product_id: int,
        delivery_id: int,
    ) -> ProductInDeliverySchema:
        query = (
            select(self._collection)
            .where(
                and_(
                    self._collection.productid == product_id,
                    self._collection.deliveryid == delivery_id
                )
            )
        )

        product = await session.scalar(query)

        if not product:
            raise ProductInDeliveryNotFound(product_id=product_id, delivery_id=delivery_id)

        return ProductInDeliverySchema.model_validate(obj=product)

    async def get_products_by_delivery(
        self,
        session: AsyncSession,
        delivery_id: int,
    ) -> list[ProductInDeliverySchema]:
        query = (
            select(self._collection)
            .where(self._collection.deliveryid == delivery_id)
        )

        products = await session.scalars(query)

        return [ProductInDeliverySchema.model_validate(obj=product) for product in products.all()]

    async def create_product_in_delivery(
        self,
        session: AsyncSession,
        product: ProductInDeliveryCreate,
    ) -> ProductInDeliverySchema:
        query = (
            insert(self._collection)
            .values(product.model_dump())
            .returning(self._collection)
        )

        try:
            created_product = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise ProductInDeliveryAlreadyExists(
                product_id=product.productid,
                delivery_id=product.deliveryid
            )

        return ProductInDeliverySchema.model_validate(obj=created_product)

    async def update_product_in_delivery(
        self,
        session: AsyncSession,
        product_id: int,
        delivery_id: int,
        product: ProductInDeliveryCreate,
    ) -> ProductInDeliverySchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.productid == product_id,
                    self._collection.deliveryid == delivery_id
                )
            )
            .values(product.model_dump())
            .returning(self._collection)
        )

        updated_product = await session.scalar(query)

        if not updated_product:
            raise ProductInDeliveryNotFound(product_id=product_id, delivery_id=delivery_id)

        return ProductInDeliverySchema.model_validate(obj=updated_product)

    async def delete_product_in_delivery(
        self,
        session: AsyncSession,
        product_id: int,
        delivery_id: int,
    ) -> None:
        query = (
            delete(self._collection)
            .where(
                and_(
                    self._collection.productid == product_id,
                    self._collection.deliveryid == delivery_id
                )
            )
        )

        result = await session.execute(query)

        if not result.rowcount:
            raise ProductInDeliveryNotFound(product_id=product_id, delivery_id=delivery_id)

    async def get_total_cost_by_delivery(
        self,
        session: AsyncSession,
        delivery_id: int,
    ) -> Decimal:
        query = (
            select(func.sum(self._collection.cost * self._collection.count))
            .where(self._collection.deliveryid == delivery_id)
        )

        total_cost = await session.scalar(query)

        return total_cost or Decimal('0')

    async def delete_all_products_in_delivery(
        self,
        session: AsyncSession,
        delivery_id: int,
    ) -> None:
        query = delete(self._collection).where(self._collection.deliveryid == delivery_id)
        await session.execute(query)
