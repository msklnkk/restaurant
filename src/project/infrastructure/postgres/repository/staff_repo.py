from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import StaffCreate, StaffSchema
from project.infrastructure.postgres.models import Staff
from project.core.exceptions import StaffNotFound, StaffAlreadyExists


class StaffRepository:
    _collection: Type[Staff] = Staff

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_staff(
        self,
        session: AsyncSession,
    ) -> list[StaffSchema]:
        query = select(self._collection)

        staff = await session.scalars(query)

        return [StaffSchema.model_validate(obj=member) for member in staff.all()]

    async def get_staff_by_id(
        self,
        session: AsyncSession,
        staff_id: int,
    ) -> StaffSchema:
        query = (
            select(self._collection)
            .where(self._collection.staffid == staff_id)
        )

        staff = await session.scalar(query)

        if not staff:
            raise StaffNotFound(_id=staff_id)

        return StaffSchema.model_validate(obj=staff)

    async def create_staff(
        self,
        session: AsyncSession,
        staff: StaffCreate,
    ) -> StaffSchema:
        query = (
            insert(self._collection)
            .values(staff.model_dump())
            .returning(self._collection)
        )

        try:
            created_staff = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise StaffAlreadyExists(contact_info=staff.contact_info)

        return StaffSchema.model_validate(obj=created_staff)

    async def update_staff(
        self,
        session: AsyncSession,
        staff_id: int,
        staff: StaffCreate,
    ) -> StaffSchema:
        query = (
            update(self._collection)
            .where(self._collection.staffid == staff_id)
            .values(staff.model_dump())
            .returning(self._collection)
        )

        updated_staff = await session.scalar(query)

        if not updated_staff:
            raise StaffNotFound(_id=staff_id)

        return StaffSchema.model_validate(obj=updated_staff)

    async def delete_staff(
        self,
        session: AsyncSession,
        staff_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.staffid == staff_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise StaffNotFound(_id=staff_id)
