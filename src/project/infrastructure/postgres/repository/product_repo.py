from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import ProductCreate, ProductSchema
from project.infrastructure.postgres.models import Product
from project.core.exceptions import ProductNotFound, ProductAlreadyExists


class ProductRepository:
    _collection: Type[Product] = Product

    async def check_connection(
            self,
            session: AsyncSession,
    ) -> bool:
        query = "select 1;"
        result = await session.scalar(text(query))
        return True if result else False

    async def get_all_products(
            self,
            session: AsyncSession,
    ) -> list[ProductSchema]:
        query = select(self._collection)
        products = await session.scalars(query)
        return [ProductSchema.model_validate(obj=product) for product in products.all()]

    async def get_product_by_id(
            self,
            session: AsyncSession,
            product_id: int,
    ) -> ProductSchema:
        query = (
            select(self._collection)
            .where(self._collection.productid == product_id)
        )
        product = await session.scalar(query)

        if not product:
            raise ProductNotFound(_id=product_id)

        return ProductSchema.model_validate(obj=product)

    async def create_product(
            self,
            session: AsyncSession,
            product: ProductCreate,
    ) -> ProductSchema:
        query = (
            insert(self._collection)
            .values(product.model_dump())
            .returning(self._collection)
        )

        try:
            created_product = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise ProductAlreadyExists(name=product.name)

        return ProductSchema.model_validate(obj=created_product)

    async def update_product(
            self,
            session: AsyncSession,
            product_id: int,
            product: ProductCreate,
    ) -> ProductSchema:
        query = (
            update(self._collection)
            .where(self._collection.productid == product_id)
            .values(product.model_dump())
            .returning(self._collection)
        )

        updated_product = await session.scalar(query)
        await session.flush()

        if not updated_product:
            raise ProductNotFound(_id=product_id)

        return ProductSchema.model_validate(obj=updated_product)

    async def delete_product(
            self,
            session: AsyncSession,
            product_id: int,
    ) -> None:
        query = (
            delete(self._collection)
            .where(self._collection.productid == product_id)
            .returning(self._collection)
        )

        deleted_product = await session.scalar(query)
        await session.flush()

        if not deleted_product:
            raise ProductNotFound(_id=product_id)
