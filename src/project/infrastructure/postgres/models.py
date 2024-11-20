from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from project.infrastructure.postgres.database import Base


class Client(Base):
    __tablename__ = "clients"

    clientid = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    mail = Column(String)
    discount_percentage = Column(Integer)

    orders = relationship("Order", back_populates="client")

class Drink(Base):
    __tablename__ = "drinks"

    drinkid = Column(Integer, primary_key=True)
    name = Column(String)

    ordered_drinks = relationship("OrderedDrink", back_populates="drink")

class Price(Base):
    __tablename__ = "prices"

    dishid = Column(Integer, primary_key=True)
    count = Column(Integer)
    price = Column(Numeric)

    dish = relationship("Dish", back_populates="price")

class Product(Base):
    __tablename__ = "products"

    productid = Column(Integer, primary_key=True)
    name = Column(String)

    dishes = relationship("Dish", back_populates="product")
    product_deliveries = relationship("ProductInDelivery", back_populates="product")

class Staff(Base):
    __tablename__ = "staff"

    staffid = Column(Integer, primary_key=True)
    name = Column(String)
    job_title = Column(String)
    date_of_hire = Column(Date)
    salary = Column(Numeric)
    contact_info = Column(Integer)

    orders = relationship("Order", back_populates="staff")

class Supplier(Base):
    __tablename__ = "suppliers"

    supplierid = Column(Integer, primary_key=True)
    name = Column(String)
    contact_info = Column(String)
    address = Column(String)

    deliveries = relationship("Delivery", back_populates="supplier")

class Table(Base):
    __tablename__ = "tables"

    tableid = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    location = Column(String)

    orders = relationship("Order", back_populates="table")

class Delivery(Base):
    __tablename__ = "delivery"

    deliveryid = Column(Integer, ForeignKey('suppliers.supplierid'), primary_key=True)
    datedelivery = Column(Date)

    supplier = relationship("Supplier", back_populates="deliveries")
    product_deliveries = relationship("ProductInDelivery", back_populates="delivery")

class Dish(Base):
    __tablename__ = "dishes"

    dishid = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    recipe = Column(String)

    price = relationship("Price", back_populates="dish", uselist=False)
    product = relationship("Product", back_populates="dishes")
    ordered_dishes = relationship("OrderedDish", back_populates="dish")

class Order(Base):
    __tablename__ = "orders"

    orderid = Column(Integer, primary_key=True)
    tableid = Column(Integer, ForeignKey('tables.tableid'))
    order_date = Column(Date)
    total_sum = Column(Numeric)
    status = Column(String)
    staffid = Column(Integer, ForeignKey('staff.staffid'))
    clientid = Column(Integer, ForeignKey('clients.clientid'))
    payment_method = Column(String)

    table = relationship("Table", back_populates="orders")
    staff = relationship("Staff", back_populates="orders")
    client = relationship("Client", back_populates="orders")
    ordered_dishes = relationship("OrderedDish", back_populates="order")
    ordered_drinks = relationship("OrderedDrink", back_populates="order")

class ProductInDelivery(Base):
    __tablename__ = "product_in_delivery"

    productid = Column(Integer, ForeignKey('products.productid'), primary_key=True)
    deliveryid = Column(Integer, ForeignKey('delivery.deliveryid'), primary_key=True)
    count = Column(Integer)
    cost = Column(Numeric)

    product = relationship("Product", back_populates="product_deliveries")
    delivery = relationship("Delivery", back_populates="product_deliveries")
    shelf_life = relationship("ShelfLife", back_populates="product_delivery")

class ShelfLife(Base):
    __tablename__ = "shelf_life"

    shelflifeid = Column(Integer, primary_key=True)
    expirationdate = Column(Date)
    deliveryID = Column(Integer, ForeignKey('delivery.deliveryid'))

    product_delivery = relationship("ProductInDelivery", back_populates="shelf_life")

class OrderedDish(Base):
    __tablename__ = "ordered_dishes"

    orderid = Column(Integer, ForeignKey('orders.orderid'), primary_key=True)
    dishid = Column(Integer, ForeignKey('dishes.dishid'))
    count = Column(Integer)

    order = relationship("Order", back_populates="ordered_dishes")
    dish = relationship("Dish", back_populates="ordered_dishes")

class OrderedDrink(Base):
    __tablename__ = "ordered_drinks"

    orderid = Column(Integer, ForeignKey('orders.orderid'), primary_key=True)
    drinkid = Column(Integer, ForeignKey('drinks.drinkid'))
    count = Column(Integer)

    order = relationship("Order", back_populates="ordered_drinks")
    drink = relationship("Drink", back_populates="ordered_drinks")