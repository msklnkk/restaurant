from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError


from project.schemas.user import TableCreate, TableSchema
from project.infrastructure.postgres.models import Table
from project.core.exceptions import TableNotFound, TableAlreadyExists


class TableRepository:
    _collection: Type[Table] = Table

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_tables(
        self,
        session: AsyncSession,
    ) -> list[TableSchema]:
        query = select(self._collection)

        tables = await session.scalars(query)

        return [TableSchema.model_validate(obj=table) for table in tables.all()]

    async def get_table_by_id(
        self,
        session: AsyncSession,
        table_id: int,
    ) -> TableSchema:
        query = (
            select(self._collection)
            .where(self._collection.tableid == table_id)
        )

        table = await session.scalar(query)

        if not table:
            raise TableNotFound(_id=table_id)

        return TableSchema.model_validate(obj=table)

    async def create_table(
        self,
        session: AsyncSession,
        table: TableCreate,
    ) -> TableSchema:
        query = (
            insert(self._collection)
            .values(table.model_dump())
            .returning(self._collection)
        )

        try:
            created_table = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise TableAlreadyExists(location=table.location)

        return TableSchema.model_validate(obj=created_table)

    async def update_table(
        self,
        session: AsyncSession,
        table_id: int,
        table: TableCreate,
    ) -> TableSchema:
        query = (
            update(self._collection)
            .where(self._collection.tableid == table_id)
            .values(table.model_dump())
            .returning(self._collection)
        )

        updated_table = await session.scalar(query)

        if not updated_table:
            raise TableNotFound(_id=table_id)

        return TableSchema.model_validate(obj=updated_table)

    async def delete_table(
        self,
        session: AsyncSession,
        table_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.tableid == table_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise TableNotFound(_id=table_id)
