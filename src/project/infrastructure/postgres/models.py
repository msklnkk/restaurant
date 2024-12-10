from sqlalchemy import ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint, false
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from decimal import Decimal
from project.infrastructure.postgres.database import Base


class Client(Base):
    __tablename__ = "clients"

    clientid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    mail: Mapped[str] = mapped_column(nullable=True)
    discount_percentage: Mapped[int] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=false())


class Drink(Base):
    __tablename__ = "drinks"

    drinkid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)


class Price(Base):
    __tablename__ = "prices"
    priceid: Mapped[int] = mapped_column(primary_key=True)
    dishid: Mapped[int] = mapped_column(ForeignKey("dishes.dishid"))
    price: Mapped[Decimal] = mapped_column(nullable=True)
    valid_from: Mapped[date] = mapped_column(nullable=True)
    valid_to: Mapped[date] = mapped_column(nullable=True)
    price_type: Mapped[str] = mapped_column(nullable=True)  # regular, business_lunch, etc.


class Product(Base):
    __tablename__ = "products"

    productid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)


class Staff(Base):
    __tablename__ = "staff"

    staffid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    job_title: Mapped[str] = mapped_column(nullable=True)
    date_of_hire: Mapped[date] = mapped_column(nullable=True)
    salary: Mapped[Decimal] = mapped_column(nullable=True)
    contact_info: Mapped[str] = mapped_column(nullable=True)


class Supplier(Base):
    __tablename__ = "suppliers"

    supplierid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    contact_info: Mapped[str] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)


class Table(Base):
    __tablename__ = "tables"

    tableid: Mapped[int] = mapped_column(primary_key=True)
    capacity: Mapped[int] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)


class Delivery(Base):
    __tablename__ = "delivery"

    deliveryid: Mapped[int] = mapped_column(ForeignKey("suppliers.supplierid"), primary_key=True)
    datedelivery: Mapped[date] = mapped_column(nullable=True)


class DishProducts(Base):
    __tablename__ = "dish_products"
    dishid: Mapped[int] = mapped_column(ForeignKey("dishes.dishid"), primary_key=True)
    productid: Mapped[int] = mapped_column(ForeignKey("products.productid"), primary_key=True)
    quantity: Mapped[int] = mapped_column(nullable=True)  # количество продукта в блюде


class Dish(Base):
    __tablename__ = "dishes"
    dishid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=True)
    type: Mapped[str] = mapped_column(nullable=True)
    recipe: Mapped[str] = mapped_column(nullable=True)


class Order(Base):
    __tablename__ = "orders"

    orderid: Mapped[int] = mapped_column(primary_key=True)
    tableid: Mapped[int] = mapped_column(ForeignKey("tables.tableid"), nullable=True)
    order_date: Mapped[date] = mapped_column(nullable=True)
    total_sum: Mapped[Decimal] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
    staffid: Mapped[int] = mapped_column(ForeignKey("staff.staffid"), nullable=True)
    clientid: Mapped[int] = mapped_column(ForeignKey("clients.clientid"), nullable=True)
    payment_method: Mapped[str] = mapped_column(nullable=True)


class ProductInDelivery(Base):
    __tablename__ = "product_in_delivery"

    productid: Mapped[int] = mapped_column(ForeignKey("products.productid"), primary_key=True)
    deliveryid: Mapped[int] = mapped_column(ForeignKey("delivery.deliveryid"), primary_key=True)
    count: Mapped[int] = mapped_column(nullable=True)
    cost: Mapped[Decimal] = mapped_column(nullable=True)



class ShelfLife(Base):
    __tablename__ = "shelf_life"

    shelflifeid: Mapped[int] = mapped_column()
    expirationdate: Mapped[date] = mapped_column(nullable=True)
    deliveryID: Mapped[int] = mapped_column(nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('shelflifeid', 'deliveryID'),  # Составной первичный ключ
        ForeignKeyConstraint(
            ['shelflifeid', 'deliveryID'],
            ['product_in_delivery.productid', 'product_in_delivery.deliveryid']
        ),
    )


class OrderedDish(Base):
    __tablename__ = "ordered_dishes"
    orderid: Mapped[int] = mapped_column(ForeignKey("orders.orderid"), primary_key=True)
    dishid: Mapped[int] = mapped_column(ForeignKey("dishes.dishid"), primary_key=True)
    count: Mapped[int] = mapped_column(nullable=True)


class OrderedDrink(Base):
    __tablename__ = "ordered_drinks"
    orderid: Mapped[int] = mapped_column(ForeignKey("orders.orderid"), primary_key=True)
    drinkid: Mapped[int] = mapped_column(ForeignKey("drinks.drinkid"), primary_key=True)
    count: Mapped[int] = mapped_column(nullable=True)