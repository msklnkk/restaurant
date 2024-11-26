from typing import Type
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import ClientCreate, Client, Drink, DrinkCreate, Price, PriceCreate
from project.infrastructure.postgres.models import Client, Drink, Price

from project.core.exceptions import UserNotFound, UserAlreadyExists, DrinkNotFound, DrinkAlreadyExists
from project.core.exceptions import PriceNotFound, PriceAlreadyExists

class ClientRepository:
    @staticmethod
    def get_client(db: Session, client_id: int):
        return db.query(Client).filter(Client.clientid == client_id).first()

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Client).offset(skip).limit(limit).all()

    @staticmethod
    def create_client(db: Session, client: ClientCreate):
        db_client = Client(**client.dict())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    @staticmethod
    def update_client(db: Session, client_id: int, client: ClientCreate):
        db_client = db.query(Client).filter(Client.clientid == client_id).first()
        if db_client:
            for key, value in client.dict().items():
                setattr(db_client, key, value)
            db.commit()
            db.refresh(db_client)
        return db_client

    @staticmethod
    def delete_client(db: Session, client_id: int):
        db_client = db.query(Client).filter(Client.clientid == client_id).first()
        if db_client:
            db.delete(db_client)
            db.commit()
            return True
        return False


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
    ) -> list[Drink]:
        query = select(self._collection)

        drinks = await session.scalars(query)

        return [Drink.from_orm(drink) for drink in drinks.all()]

    async def get_drink_by_id(
        self,
        session: AsyncSession,
        drink_id: int,
    ) -> Drink:
        query = (
            select(self._collection)
            .where(self._collection.drinkid == drink_id)
        )

        drink = await session.scalar(query)

        if not drink:
            raise DrinkNotFound(_id=drink_id)

        return Drink.from_orm(drink)

    async def create_drink(
        self,
        session: AsyncSession,
        drink: DrinkCreate,
    ) -> Drink:
        query = (
            insert(self._collection)
            .values(drink.dict(exclude_unset=True))
            .returning(self._collection)
        )

        try:
            created_drink = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise DrinkAlreadyExists(name=drink.name)

        return Drink.from_orm(created_drink)

    async def update_drink(
        self,
        session: AsyncSession,
        drink_id: int,
        drink: DrinkCreate,
    ) -> Drink:
        query = (
            update(self._collection)
            .where(self._collection.drinkid == drink_id)
            .values(drink.dict(exclude_unset=True))
            .returning(self._collection)
        )

        updated_drink = await session.scalar(query)

        if not updated_drink:
            raise DrinkNotFound(_id=drink_id)

        return Drink.from_orm(updated_drink)

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
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_prices(
        self,
        session: AsyncSession,
    ) -> list[Price]:
        query = select(self._collection)

        prices = await session.scalars(query)

        return [Price.from_orm(price) for price in prices.all()]

    async def get_price_by_id(
        self,
        session: AsyncSession,
        dishid: int,
    ) -> Price:
        query = (
            select(self._collection)
            .where(self._collection.dishid == dishid)
        )

        price = await session.scalar(query)

        if not price:
            raise PriceNotFound(_id=dishid)

        return Price.from_orm(price)

    async def create_price(
        self,
        session: AsyncSession,
        price: PriceCreate,
    ) -> Price:
        query = (
            insert(self._collection)
            .values(price.dict(exclude_unset=True))
            .returning(self._collection)
        )

        try:
            created_price = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise PriceAlreadyExists(dish_id=created_price.dishid)

        return Price.from_orm(created_price)

    async def update_price(
        self,
        session: AsyncSession,
        dishid: int,
        price: PriceCreate,
    ) -> Price:
        query = (
            update(self._collection)
            .where(self._collection.dishid == dishid)
            .values(price.dict(exclude_unset=True))
            .returning(self._collection)
        )

        updated_price = await session.scalar(query)

        if not updated_price:
            raise PriceNotFound(_id=dishid)

        return Price.from_orm(updated_price)

    async def delete_price(
        self,
        session: AsyncSession,
        dishid: int
    ) -> None:
        query = delete(self._collection).where(self._collection.dishid == dishid)

        result = await session.execute(query)

        if not result.rowcount:
            raise PriceNotFound(_id=dishid)
