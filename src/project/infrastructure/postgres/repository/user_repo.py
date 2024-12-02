from typing import Type
from sqlalchemy.orm import Session
from datetime import date
from decimal import Decimal
from sqlalchemy import func

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete, and_
from sqlalchemy.exc import IntegrityError

from project.schemas.user import ClientCreate, ClientSchema, DrinkSchema, DrinkCreate, PriceSchema, PriceCreate
from project.schemas.user import ProductCreate, ProductSchema, StaffCreate, StaffSchema, SupplierCreate, SupplierSchema
from project.schemas.user import TableCreate, TableSchema, DeliveryCreate, DeliverySchema, DishProductsCreate, DishProductsSchema
from project.schemas.user import DishCreate, DishSchema, OrderCreate, OrderSchema, ProductInDeliveryCreate, ProductInDeliverySchema
from project.schemas.user import ShelfLifeCreate, ShelfLifeSchema, OrderedDrinkCreate, OrderedDrinkSchema, OrderedDishCreate, OrderedDishSchema

from project.infrastructure.postgres.models import Client, Drink, Price, Product, Staff, Supplier, Table, Delivery
from project.infrastructure.postgres.models import DishProducts, Dish, Order, ProductInDelivery, ShelfLife, OrderedDrink, OrderedDish


from project.core.exceptions import UserNotFound, UserAlreadyExists, DrinkNotFound, DrinkAlreadyExists, ProductNotFound, ProductAlreadyExists
from project.core.exceptions import StaffNotFound, StaffAlreadyExists, SupplierNotFound, SupplierAlreadyExists, OrderNotFound, OrderAlreadyExists
from project.core.exceptions import TableNotFound, TableAlreadyExists, DeliveryNotFound, DeliveryAlreadyExists
from project.core.exceptions import PriceNotFound, PriceAlreadyExists, DishProductNotFound, DishProductAlreadyExists, DishNotFound, DishAlreadyExists
from project.core.exceptions import ProductInDeliveryNotFound, ProductInDeliveryAlreadyExists, ShelfLifeNotFound, ShelfLifeAlreadyExists
from project.core.exceptions import OrderedDishNotFound, OrderedDishAlreadyExists, OrderedDrinkNotFound, OrderedDrinkAlreadyExists



class ClientRepository:
    _collection: Type[Client] = Client

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_users(
        self,
        session: AsyncSession,
    ) -> list[ClientSchema]:
        query = select(self._collection)

        users = await session.scalars(query)

        return [ClientSchema.model_validate(obj=user) for user in users.all()]

    async def get_user_by_id(
        self,
        session: AsyncSession,
        user_id: int,
    ) -> ClientSchema:
        query = (
            select(self._collection)
            .where(self._collection.id == user_id)
        )

        user = await session.scalar(query)

        if not user:
            raise UserNotFound(_id=user_id)

        return ClientSchema.model_validate(obj=user)

    async def create_user(
        self,
        session: AsyncSession,
        user: ClientCreate,
    ) -> ClientSchema:
        query = (
            insert(self._collection)
            .values(user.model_dump())
            .returning(self._collection)
        )

        try:
            created_user = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise UserAlreadyExists(email=user.email)

        return ClientSchema.model_validate(obj=created_user)

    async def update_user(
        self,
        session: AsyncSession,
        user_id: int,
        user: ClientCreate,
    ) -> ClientSchema:
        query = (
            update(self._collection)
            .where(self._collection.id == user_id)
            .values(user.model_dump())
            .returning(self._collection)
        )

        updated_user = await session.scalar(query)

        if not updated_user:
            raise UserNotFound(_id=user_id)

        return ClientSchema.model_validate(obj=updated_user)

    async def delete_user(
        self,
        session: AsyncSession,
        user_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.id == user_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise UserNotFound(_id=user_id)

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
    ) -> list[DrinkSchema]:
        query = select(self._collection)

        drinks = await session.scalars(query)

        return [DrinkSchema.model_validate(obj=drink) for drink in drinks.all()]

    async def get_drink_by_id(
        self,
        session: AsyncSession,
        drink_id: int,
    ) -> DrinkSchema:
        query = (
            select(self._collection)
            .where(self._collection.drinkid == drink_id)
        )

        drink = await session.scalar(query)

        if not drink:
            raise DrinkNotFound(_id=drink_id)

        return DrinkSchema.model_validate(obj=drink)

    async def create_drink(
        self,
        session: AsyncSession,
        drink: DrinkCreate,
    ) -> DrinkSchema:
        query = (
            insert(self._collection)
            .values(drink.model_dump(exclude_unset=True))
            .returning(self._collection)
        )

        try:
            created_drink = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise DrinkAlreadyExists(name=drink.name)

        return DrinkSchema.model_validate(obj=created_drink)

    async def update_drink(
        self,
        session: AsyncSession,
        drink_id: int,
        drink: DrinkCreate,
    ) -> DrinkSchema:
        query = (
            update(self._collection)
            .where(self._collection.drinkid == drink_id)
            .values(drink.model_dump(exclude_unset=True))
            .returning(self._collection)
        )

        updated_drink = await session.scalar(query)

        if not updated_drink:
            raise DrinkNotFound(_id=drink_id)

        return DrinkSchema.model_validate(obj=updated_drink)

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
        session: AsyncSession,я
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



class DishRepository:
    _collection: Type[Dish] = Dish

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_dishes(
        self,
        session: AsyncSession,
    ) -> list[DishSchema]:
        query = select(self._collection)

        dishes = await session.scalars(query)

        return [DishSchema.model_validate(obj=dish) for dish in dishes.all()]

    async def get_dish_by_id(
        self,
        session: AsyncSession,
        dish_id: int,
    ) -> DishSchema:
        query = (
            select(self._collection)
            .where(self._collection.dishid == dish_id)
        )

        dish = await session.scalar(query)

        if not dish:
            raise DishNotFound(_id=dish_id)

        return DishSchema.model_validate(obj=dish)

    async def get_dishes_by_type(
        self,
        session: AsyncSession,
        dish_type: str,
    ) -> list[DishSchema]:
        query = (
            select(self._collection)
            .where(self._collection.type == dish_type)
        )

        dishes = await session.scalars(query)

        return [DishSchema.model_validate(obj=dish) for dish in dishes.all()]

    async def create_dish(
        self,
        session: AsyncSession,
        dish: DishCreate,
    ) -> DishSchema:
        query = (
            insert(self._collection)
            .values(dish.model_dump())
            .returning(self._collection)
        )

        try:
            created_dish = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise DishAlreadyExists(name=dish.name)

        return DishSchema.model_validate(obj=created_dish)

    async def update_dish(
        self,
        session: AsyncSession,
        dish_id: int,
        dish: DishCreate,
    ) -> DishSchema:
        query = (
            update(self._collection)
            .where(self._collection.dishid == dish_id)
            .values(dish.model_dump())
            .returning(self._collection)
        )

        updated_dish = await session.scalar(query)

        if not updated_dish:
            raise DishNotFound(_id=dish_id)

        return DishSchema.model_validate(obj=updated_dish)

    async def delete_dish(
        self,
        session: AsyncSession,
        dish_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.dishid == dish_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise DishNotFound(_id=dish_id)

    async def search_dishes_by_name(
        self,
        session: AsyncSession,
        name: str
    ) -> list[DishSchema]:
        query = (
            select(self._collection)
            .where(self._collection.name.ilike(f"%{name}%"))
        )

        dishes = await session.scalars(query)

        return [DishSchema.model_validate(obj=dish) for dish in dishes.all()]




class OrderRepository:
    _collection: Type[Order] = Order

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_orders(
        self,
        session: AsyncSession,
    ) -> list[OrderSchema]:
        query = select(self._collection)

        orders = await session.scalars(query)

        return [OrderSchema.model_validate(obj=order) for order in orders.all()]

    async def get_order_by_id(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> OrderSchema:
        query = (
            select(self._collection)
            .where(self._collection.orderid == order_id)
        )

        order = await session.scalar(query)

        if not order:
            raise OrderNotFound(_id=order_id)

        return OrderSchema.model_validate(obj=order)

    async def create_order(
        self,
        session: AsyncSession,
        order: OrderCreate,
    ) -> OrderSchema:
        query = (
            insert(self._collection)
            .values(order.model_dump())
            .returning(self._collection)
        )

        try:
            created_order = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise OrderAlreadyExists(
                table_id=order.tableid,
                date=order.order_date.strftime("%Y-%m-%d")
            )

        return OrderSchema.model_validate(obj=created_order)

    async def update_order(
        self,
        session: AsyncSession,
        order_id: int,
        order: OrderCreate,
    ) -> OrderSchema:
        query = (
            update(self._collection)
            .where(self._collection.orderid == order_id)
            .values(order.model_dump())
            .returning(self._collection)
        )

        updated_order = await session.scalar(query)

        if not updated_order:
            raise OrderNotFound(_id=order_id)

        return OrderSchema.model_validate(obj=updated_order)

    async def delete_order(
        self,
        session: AsyncSession,
        order_id: int
    ) -> None:
        query = delete(self._collection).where(self._collection.orderid == order_id)

        result = await session.execute(query)

        if not result.rowcount:
            raise OrderNotFound(_id=order_id)

    async def get_orders_by_date(
        self,
        session: AsyncSession,
        order_date: date,
    ) -> list[OrderSchema]:
        query = (
            select(self._collection)
            .where(self._collection.order_date == order_date)
        )

        orders = await session.scalars(query)

        return [OrderSchema.model_validate(obj=order) for order in orders.all()]

    async def get_orders_by_status(
        self,
        session: AsyncSession,
        status: str,
    ) -> list[OrderSchema]:
        query = (
            select(self._collection)
            .where(self._collection.status == status)
        )

        orders = await session.scalars(query)

        return [OrderSchema.model_validate(obj=order) for order in orders.all()]

    async def get_orders_by_client(
        self,
        session: AsyncSession,
        client_id: int,
    ) -> list[OrderSchema]:
        query = (
            select(self._collection)
            .where(self._collection.clientid == client_id)
        )

        orders = await session.scalars(query)

        return [OrderSchema.model_validate(obj=order) for order in orders.all()]

    async def get_orders_by_staff(
        self,
        session: AsyncSession,
        staff_id: int,
    ) ->list[OrderSchema]:
        query = (
            select(self._collection)
            .where(self._collection.staffid == staff_id)
        )

        orders = await session.scalars(query)

        return [OrderSchema.model_validate(obj=order) for order in orders.all()]

    async def update_order_status(
        self,
        session: AsyncSession,
        order_id: int,
        status: str,
    ) -> OrderSchema:
        query = (
            update(self._collection)
            .where(self._collection.orderid == order_id)
            .values(status=status)
            .returning(self._collection)
        )

        updated_order = await session.scalar(query)

        if not updated_order:
            raise OrderNotFound(_id=order_id)

        return OrderSchema.model_validate(obj=updated_order)



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




class OrderedDishRepository:
    _collection: Type[OrderedDish] = OrderedDish

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_ordered_dishes(
        self,
        session: AsyncSession,
    ) -> list[OrderedDishSchema]:
        query = select(self._collection)

        ordered_dishes = await session.scalars(query)

        return [OrderedDishSchema.model_validate(obj=dish) for dish in ordered_dishes.all()]

    async def get_ordered_dish(
        self,
        session: AsyncSession,
        order_id: int,
        dish_id: int,
    ) -> OrderedDishSchema:
        query = (
            select(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.dishid == dish_id
                )
            )
        )

        ordered_dish = await session.scalar(query)

        if not ordered_dish:
            raise OrderedDishNotFound(dish_id=dish_id, order_id=order_id)

        return OrderedDishSchema.model_validate(obj=ordered_dish)

    async def get_dishes_by_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> list[OrderedDishSchema]:
        query = (
            select(self._collection)
            .where(self._collection.orderid == order_id)
        )

        ordered_dishes = await session.scalars(query)

        return [OrderedDishSchema.model_validate(obj=dish) for dish in ordered_dishes.all()]

    async def create_ordered_dish(
        self,
        session: AsyncSession,
        ordered_dish: OrderedDishCreate,
    ) -> OrderedDishSchema:
        query = (
            insert(self._collection)
            .values(ordered_dish.model_dump())
            .returning(self._collection)
        )

        try:
            created_ordered_dish = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise OrderedDishAlreadyExists(
                dish_id=ordered_dish.dishid,
                order_id=ordered_dish.orderid
            )

        return OrderedDishSchema.model_validate(obj=created_ordered_dish)

    async def update_ordered_dish(
        self,
        session: AsyncSession,
        order_id: int,
        dish_id: int,
        ordered_dish: OrderedDishCreate,
    ) -> OrderedDishSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.dishid == dish_id
                )
            )
            .values(ordered_dish.model_dump())
            .returning(self._collection)
        )

        updated_ordered_dish = await session.scalar(query)

        if not updated_ordered_dish:
            raise OrderedDishNotFound(dish_id=dish_id, order_id=order_id)

        return OrderedDishSchema.model_validate(obj=updated_ordered_dish)

    async def delete_ordered_dish(
        self,
        session: AsyncSession,
        order_id: int,
        dish_id: int,
    ) -> None:
        query = (
            delete(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.dishid == dish_id
                )
            )
        )

        result = await session.execute(query)

        if not result.rowcount:
            raise OrderedDishNotFound(dish_id=dish_id, order_id=order_id)

    async def update_dish_count(
        self,
        session: AsyncSession,
        order_id: int,
        dish_id: int,count: int,
    ) -> OrderedDishSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.dishid == dish_id
                )
            )
            .values(count=count)
            .returning(self._collection)
        )

        updated_ordered_dish = await session.scalar(query)

        if not updated_ordered_dish:
            raise OrderedDishNotFound(dish_id=dish_id, order_id=order_id)

        return OrderedDishSchema.model_validate(obj=updated_ordered_dish)

    async def delete_dishes_from_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> None:
        query = delete(self._collection).where(self._collection.orderid == order_id)
        await session.execute(query)




class OrderedDrinkRepository:
    _collection: Type[OrderedDrink] = OrderedDrink

    async def check_connection(
        self,
        session: AsyncSession,
    ) -> bool:
        query = "select 1;"

        result = await session.scalar(text(query))

        return True if result else False

    async def get_all_ordered_drinks(
        self,
        session: AsyncSession,
    ) -> list[OrderedDrinkSchema]:
        query = select(self._collection)

        ordered_drinks = await session.scalars(query)

        return [OrderedDrinkSchema.model_validate(obj=drink) for drink in ordered_drinks.all()]

    async def get_ordered_drink(
        self,
        session: AsyncSession,
        order_id: int,
        drink_id: int,
    ) -> OrderedDrinkSchema:
        query = (
            select(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.drinkid == drink_id
                )
            )
        )

        ordered_drink = await session.scalar(query)

        if not ordered_drink:
            raise OrderedDrinkNotFound(drink_id=drink_id, order_id=order_id)

        return OrderedDrinkSchema.model_validate(obj=ordered_drink)

    async def get_drinks_by_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> list[OrderedDrinkSchema]:
        query = (
            select(self._collection)
            .where(self._collection.orderid == order_id)
        )

        ordered_drinks = await session.scalars(query)

        return [OrderedDrinkSchema.model_validate(obj=drink) for drink in ordered_drinks.all()]

    async def create_ordered_drink(
        self,
        session: AsyncSession,
        ordered_drink: OrderedDrinkCreate,
    ) -> OrderedDrinkSchema:
        query = (
            insert(self._collection)
            .values(ordered_drink.model_dump())
            .returning(self._collection)
        )

        try:
            created_ordered_drink = await session.scalar(query)
            await session.flush()
        except IntegrityError:
            raise OrderedDrinkAlreadyExists(
                drink_id=ordered_drink.drinkid,
                order_id=ordered_drink.orderid
            )

        return OrderedDrinkSchema.model_validate(obj=created_ordered_drink)

    async def update_ordered_drink(
        self,
        session: AsyncSession,
        order_id: int,
        drink_id: int,
        ordered_drink: OrderedDrinkCreate,
    ) -> OrderedDrinkSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.drinkid == drink_id
                )
            )
            .values(ordered_drink.model_dump())
            .returning(self._collection)
        )

        updated_ordered_drink = await session.scalar(query)

        if not updated_ordered_drink:
            raise OrderedDrinkNotFound(drink_id=drink_id, order_id=order_id)

        return OrderedDrinkSchema.model_validate(obj=updated_ordered_drink)

    async def delete_ordered_drink(
        self,
        session: AsyncSession,
        order_id: int,
        drink_id: int,
    ) -> None:
        query = (
            delete(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.drinkid == drink_id
                )
            )
        )

        result = await session.execute(query)

        if not result.rowcount:
            raise OrderedDrinkNotFound(drink_id=drink_id, order_id=order_id)

    async def update_drink_count(
        self,
        session:AsyncSession,
        order_id: int,
        drink_id: int,
        count: int,
    ) -> OrderedDrinkSchema:
        query = (
            update(self._collection)
            .where(
                and_(
                    self._collection.orderid == order_id,
                    self._collection.drinkid == drink_id
                )
            )
            .values(count=count)
            .returning(self._collection)
        )

        updated_ordered_drink = await session.scalar(query)

        if not updated_ordered_drink:
            raise OrderedDrinkNotFound(drink_id=drink_id, order_id=order_id)

        return OrderedDrinkSchema.model_validate(obj=updated_ordered_drink)

    async def delete_drinks_from_order(
        self,
        session: AsyncSession,
        order_id: int,
    ) -> None:
        query = delete(self._collection).where(self._collection.orderid == order_id)
        await session.execute(query)