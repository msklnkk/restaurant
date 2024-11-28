from pydantic import BaseModel, ConfigDict
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

class ClientSchema(ClientBase):
    clientid: int

    model_config = ConfigDict(from_attributes=True)

class DrinkBase(BaseModel):
    name: Optional[str]

class DrinkCreate(DrinkBase):
    pass

class DrinkSchema(DrinkBase):
    drinkid: int

    model_config = ConfigDict(from_attributes=True)

class PriceBase(BaseModel):
    count: Optional[int]
    price: Optional[Decimal]

class PriceCreate(PriceBase):
    pass

class PriceSchema(PriceBase):
    dishid: int

    model_config = ConfigDict(from_attributes=True)

class ProductBase(BaseModel):
    name: Optional[str]

class ProductCreate(ProductBase):
    pass

class ProductSchema(ProductBase):
    productid: int

    model_config = ConfigDict(from_attributes=True)

class StaffBase(BaseModel):
    name: Optional[str]
    job_title: Optional[str]
    date_of_hire: Optional[date]
    salary: Optional[Decimal]
    contact_info: Optional[int]

class StaffCreate(StaffBase):
    pass

class StaffSchema(StaffBase):
    staffid: int

    model_config = ConfigDict(from_attributes=True)

class SupplierBase(BaseModel):
    name: Optional[str]
    contact_info: Optional[str]
    address: Optional[str]

class SupplierCreate(SupplierBase):
    pass

class SupplierSchema(SupplierBase):
    supplierid: int

    model_config = ConfigDict(from_attributes=True)

class TableBase(BaseModel):
    capacity: Optional[int]
    location: Optional[str]

class TableCreate(TableBase):
    pass

class TableSchema(TableBase):
    tableid: int

    model_config = ConfigDict(from_attributes=True)

class DeliveryBase(BaseModel):
    datedelivery: Optional[date]

class DeliveryCreate(DeliveryBase):
    pass

class DeliverySchema(DeliveryBase):
    deliveryid: int

    model_config = ConfigDict(from_attributes=True)

class DishBase(BaseModel):
    name: Optional[str]
    type: Optional[str]
    recipe: Optional[str]

class DishCreate(DishBase):
    pass

class DishSchema(DishBase):
    dishid: int

    model_config = ConfigDict(from_attributes=True)

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

class OrderSchema(OrderBase):
    orderid: int

    model_config = ConfigDict(from_attributes=True)

class ProductInDeliveryBase(BaseModel):
    count: Optional[int]
    cost: Optional[Decimal]

class ProductInDeliveryCreate(ProductInDeliveryBase):
    productid: int
    deliveryid: int

class ProductInDeliverySchema(ProductInDeliveryBase):
    productid: int
    deliveryid: int

    model_config = ConfigDict(from_attributes=True)

class ShelfLifeBase(BaseModel):
    expirationdate: Optional[date]
    deliveryID: Optional[int]

class ShelfLifeCreate(ShelfLifeBase):
    pass

class ShelfLifeSchema(ShelfLifeBase):
    shelflifeid: int

    model_config = ConfigDict(from_attributes=True)

class OrderedDishBase(BaseModel):
    dishid: Optional[int]
    count: Optional[int]

class OrderedDishCreate(OrderedDishBase):
    pass

class OrderedDishSchema(OrderedDishBase):
    orderid: int

    model_config = ConfigDict(from_attributes=True)

class OrderedDrinkBase(BaseModel):
    drinkid: Optional[int]
    count: Optional[int]

class OrderedDrinkCreate(OrderedDrinkBase):
    pass

class OrderedDrinkSchema(OrderedDrinkBase):
    orderid: int

    model_config = ConfigDict(from_attributes=True)