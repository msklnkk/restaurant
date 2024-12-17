from typing import Final
from fastapi import HTTPException, status

# Client
class UserNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Клиент с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class UserAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Клиент с почтой '{mail}' уже существует"

    def __init__(self, mail: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(mail=mail)
        super().__init__(self.message)


# Drinks
class DrinkNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Напиток с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class DrinkAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Напиток с названием '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)


# Price
class PriceNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Цена для блюда с id {id} не найдена"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class PriceAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Цена для блюда с id '{dish_id}' уже существует"

    def __init__(self, dish_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(dish_id=dish_id)
        super().__init__(self.message)



# Исключения для Product
class ProductNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Продукт с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class ProductAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Продукт с названием '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)



# Исключения для Staff
class StaffNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Сотрудник с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class StaffAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Сотрудник с контактными данными '{contact_info}' уже существует"

    def __init__(self, contact_info: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(contact_info=contact_info)
        super().__init__(self.message)



# Исключения для Supplier
class SupplierNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Поставщик с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class SupplierAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Поставщик с контактными данными '{contact_info}' уже существует"

    def __init__(self, contact_info: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(contact_info=contact_info)
        super().__init__(self.message)



# Исключения для Table
class TableNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Стол с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class TableAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Стол в локации '{location}' уже существует"

    def __init__(self, location: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(location=location)
        super().__init__(self.message)


# Исключения для Delivery
class DeliveryNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Доставка с id {id} не найдена"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class DeliveryAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Доставка для поставщика с id '{supplier_id}' на дату '{date}' уже существует"

    def __init__(self, supplier_id: int, date: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(supplier_id=supplier_id, date=date)
        super().__init__(self.message)


# Исключения для DishProducts
class DishProductNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Связь блюда (id: {dish_id}) с продуктом (id: {product_id}) не найдена"
    message: str

    def __init__(self, dish_id: int | str, product_id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(dish_id=dish_id, product_id=product_id)
        super().__init__(self.message)


class DishProductAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Связь блюда (id: {dish_id}) с продуктом (id: {product_id}) уже существует"

    def __init__(self, dish_id: int, product_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(dish_id=dish_id, product_id=product_id)
        super().__init__(self.message)


# Исключения для Dish
class DishNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Блюдо с id {id} не найдено"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class DishAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Блюдо с названием '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(name=name)
        super().__init__(self.message)



# Исключения для Order
class OrderNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Заказ с id {id} не найден"
    message: str

    def __init__(self, _id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class OrderAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Заказ для стола {table_id} на дату {date} уже существует"

    def __init__(self, table_id: int, date: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(table_id=table_id, date=date)
        super().__init__(self.message)


# Исключения для ProductInDelivery
class ProductInDeliveryNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Продукт (id: {product_id}) в поставке (id: {delivery_id}) не найден"
    message: str

    def __init__(self, product_id: int | str, delivery_id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(product_id=product_id, delivery_id=delivery_id)
        super().__init__(self.message)


class ProductInDeliveryAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Продукт (id: {product_id}) в поставке (id: {delivery_id}) уже существует"

    def __init__(self, product_id: int, delivery_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(product_id=product_id, delivery_id=delivery_id)
        super().__init__(self.message)


# Исключения для ShelfLife
class ShelfLifeNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Срок годности (id: {shelf_id}) для поставки (id: {delivery_id}) не найден"
    message: str

    def __init__(self, shelf_id: int | str, delivery_id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(shelf_id=shelf_id, delivery_id=delivery_id)
        super().__init__(self.message)


class ShelfLifeAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Срок годности (id: {shelf_id}) для поставки (id: {delivery_id}) уже существует"

    def __init__(self, shelf_id: int, delivery_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(shelf_id=shelf_id, delivery_id=delivery_id)
        super().__init__(self.message)


# Исключения для OrderedDish
class OrderedDishNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Блюдо (id: {dish_id}) в заказе (id: {order_id}) не найдено"
    message: str

    def __init__(self, dish_id: int | str, order_id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(dish_id=dish_id, order_id=order_id)
        super().__init__(self.message)


class OrderedDishAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Блюдо (id: {dish_id}) в заказе (id: {order_id}) уже существует"

    def __init__(self, dish_id: int, order_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(dish_id=dish_id, order_id=order_id)
        super().__init__(self.message)


# Исключения для OrderedDrink
class OrderedDrinkNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Напиток (id: {drink_id}) в заказе (id: {order_id}) не найден"
    message: str

    def __init__(self, drink_id: int | str, order_id: int | str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(drink_id=drink_id, order_id=order_id)
        super().__init__(self.message)


class OrderedDrinkAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Напиток (id: {drink_id}) в заказе (id: {order_id}) уже существует"

    def __init__(self, drink_id: int, order_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(drink_id=drink_id, order_id=order_id)
        super().__init__(self.message)






class DatabaseError(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Произошла ошибка в базе данных: {message}"
    def __init__(self, message: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(message=message)
        super().__init__(self.message)
class CredentialsException(HTTPException):
    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )