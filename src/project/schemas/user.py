from pydantic import BaseModel
from datetime import date
from typing import Optional
from decimal import Decimal

class ClientBase(BaseModel):
    name: Optional[str]
    phone_number: Optional[str]
    mail: Optional[str]
    discount_percentage: Optional[int]

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    clientid: int

    class Config:
        orm_mode = True

class DrinkBase(BaseModel):
    name: Optional[str]

class DrinkCreate(DrinkBase):
    pass

class Drink(DrinkBase):
    drinkid: int

    class Config:
        orm_mode = True

class PriceBase(BaseModel):
    count: Optional[int]
    price: Optional[Decimal]

class PriceCreate(PriceBase):
    pass

class Price(PriceBase):
    dishid: int

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: Optional[str]

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    productid: int

    class Config:
        orm_mode = True

class StaffBase(BaseModel):
    name: Optional[str]
    job_title: Optional[str]
    date_of_hire: Optional[date]
    salary: Optional[Decimal]
    contact_info: Optional[int]

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    staffid: int

    class Config:
        orm_mode = True

class SupplierBase(BaseModel):
    name: Optional[str]
    contact_info: Optional[str]
    address: Optional[str]

class SupplierCreate(SupplierBase):
    pass

class Supplier(SupplierBase):
    supplierid: int

    class Config:
        orm_mode = True

class TableBase(BaseModel):
    capacity: Optional[int]
    location: Optional[str]

class TableCreate(TableBase):
    pass

class Table(TableBase):
    tableid: int

    class Config:
        orm_mode = True

class DeliveryBase(BaseModel):
    datedelivery: Optional[date]

class DeliveryCreate(DeliveryBase):
    pass

class Delivery(DeliveryBase):
    deliveryid: int

    class Config:
        orm_mode = True

class DishBase(BaseModel):
    name: Optional[str]
    type: Optional[str]
    recipe: Optional[str]

class DishCreate(DishBase):
    pass

class Dish(DishBase):
    dishid: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    tableid: Optional[int]
    order_date: Optional[date]
    total_sum: Optional[Decimal]
    status: Optional[str]
    staffid: Optional[int]
    clientid: Optional[int]
    payment_method: Optional[str]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    orderid: int

    class Config:
        orm_mode = True

class ProductInDeliveryBase(BaseModel):
    count: Optional[int]
    cost: Optional[Decimal]

class ProductInDeliveryCreate(ProductInDeliveryBase):
    productid: int
    deliveryid: int

class ProductInDelivery(ProductInDeliveryBase):
    productid: int
    deliveryid: int

    class Config:
        orm_mode = True

class ShelfLifeBase(BaseModel):
    expirationdate: Optional[date]
    deliveryID: Optional[int]

class ShelfLifeCreate(ShelfLifeBase):
    pass

class ShelfLife(ShelfLifeBase):
    shelflifeid: int

    class Config:
        orm_mode = True

class OrderedDishBase(BaseModel):
    dishid: Optional[int]
    count: Optional[int]

class OrderedDishCreate(OrderedDishBase):
    pass

class OrderedDish(OrderedDishBase):
    orderid: int

    class Config:
        orm_mode = True

class OrderedDrinkBase(BaseModel):
    drinkid: Optional[int]
    count: Optional[int]

class OrderedDrinkCreate(OrderedDrinkBase):
    pass

class OrderedDrink(OrderedDrinkBase):
    orderid: int

    class Config:
        orm_mode = True