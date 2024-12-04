from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import SupplierCreate, SupplierSchema
from project.infrastructure.postgres.models import Supplier
from project.core.exceptions import SupplierNotFound, SupplierAlreadyExists



class SupplierRepository:
    _collection: Type[Supplier] = Supplier

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_suppliers(
        self,
        session: AsyncSession,
    ) -> list[SupplierSchema]:
        query = select(self._collection)

        suppliers = await session.scalars(query)

        return [SupplierSchema.model_validate(obj=supplier) for supplier in suppliers.all()]

    async def get_supplier_by_id(
        self,
        session: AsyncSession,
        supplier_id: int,
    ) -> SupplierSchema:
        query = (
            select(self._collection)
            .where(self._collection.supplierid == supplier_id)
        )

        supplier = await session.scalar(query)

        if not supplier:
            raise SupplierNotFound(_id=supplier_id)

        return SupplierSchema.model_validate(obj=supplier)

    async def create_supplier(
        self,
        session: AsyncSession,
        supplier: SupplierCreate,
    ) -> SupplierSchema:
        query = (
            insert(self._collection)
            .values(supplier.model_dump())
            .returning(self._collection)
        )

        try:
            created_supplier = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise SupplierAlreadyExists(contact_info=supplier.contact_info)

        return SupplierSchema.model_validate(obj=created_supplier)

    async def update_supplier(
        self,
        session: AsyncSession,
        supplier_id: int,
        supplier: SupplierCreate,
    ) -> SupplierSchema:
        query = (
            update(self._collection)
            .where(self._collection.supplierid == supplier_id)
            .values(supplier.model_dump())
            .returning(self._collection)
        )

        updated_supplier = await session.scalar(query)

        if not updated_supplier:
            raise SupplierNotFound(_id=supplier_id)

        return SupplierSchema.model_validate(obj=updated_supplier)

    async def delete_supplier(
        self,
        session: AsyncSession,
        supplier_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.supplierid == supplier_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise SupplierNotFound(_id=supplier_id)
