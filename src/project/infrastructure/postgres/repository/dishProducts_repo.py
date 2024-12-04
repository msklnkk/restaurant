from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, and_
from sqlalchemy.exc import IntegrityError

from project.schemas.user import DishProductsCreate, DishProductsSchema
from project.infrastructure.postgres.models import DishProducts
from project.core.exceptions import DishProductNotFound, DishProductAlreadyExists


class DishProductsRepository:
    _collection: Type[DishProducts] = DishProducts

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_dish_products(
        self,
        session: AsyncSession,
    ) -> list[DishProductsSchema]:
        query = select(self._collection)

        dish_products = await session.scalars(query)

        return [DishProductsSchema.model_validate(obj=dp) for dp in dish_products.all()]

    async def get_dish_product(
        self,
        session: AsyncSession,
        dish_id: int,
        product_id: int,
    ) -> DishProductsSchema:
        query = (
            select(self._collection)
            .where(
                and_(
                    self._collection.dishid == dish_id,
                    self._collection.productid == product_id
                )
            )
        )

        dish_product = await session.scalar(query)

        if not dish_product:
            raise DishProductNotFound(dish_id=dish_id, product_id=product_id)

        return DishProductsSchema.model_validate(obj=dish_product)

    async def get_products_for_dish(
        self,
        session: AsyncSession,
        dish_id: int,
    ) -> list[DishProductsSchema]:
        query = (
            select(self._collection)
            .where(self._collection.dishid == dish_id)
        )

        dish_products = await session.scalars(query)

        return [DishProductsSchema.model_validate(obj=dp) for dp in dish_products.all()]

    async def create_dish_product(
        self,
        session: AsyncSession,
        dish_product: DishProductsCreate,
    ) -> DishProductsSchema:
        query = (
            insert(self._collection)
            .values(dish_product.model_dump())
            .returning(self._collection)
        )

        try:
            created_dish_product = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise DishProductAlreadyExists(
                dish_id=dish_product.dishid,
                product_id=dish_product.productid
            )

        return DishProductsSchema.model_validate(obj=created_dish_product)

    async def update_dish_product(
        self,
        session: AsyncSession,
        dish_id: int,
        product_id: int,
        dish_product: DishProductsCreate,
    ) -> DishProductsSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.dishid == dish_id,
                    self._collection.productid == product_id
                )
            )
            .values(dish_product.model_dump())
            .returning(self._collection)
        )

        updated_dish_product = await session.scalar(query)

        if not updated_dish_product:
            raise DishProductNotFound(dish_id=dish_id, product_id=product_id)

        return DishProductsSchema.model_validate(obj=updated_dish_product)

    async def delete_dish_product(
        self,
        session: AsyncSession,
        dish_id: int,
        product_id: int,
    ) -> None:
        query = (
            delete(self._collection)
            .where(
                and_(
                    self._collection.dishid == dish_id,
                    self._collection.productid == product_id
                )
            )
        )

        result = await session.execute(query)

        if not result.rowcount:
            raise DishProductNotFound(dish_id=dish_id, product_id=product_id)

    async def delete_all_products_for_dish(
        self,
        session: AsyncSession,
        dish_id: int,
    ) -> None:
        query = delete(self._collection).where(self._collection.dishid == dish_id)
        await session.execute(query)
