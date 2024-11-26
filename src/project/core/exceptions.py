from typing import Final

# Client
class UserNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Клиент с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().__init__(self.message)


class UserAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Клиент с почтой '{email}' уже существует"

    def __init__(self, email: str) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(email=email)
        super().__init__(self.message)


# Drinks
class DrinkNotFound(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Напиток с id {id} не найден"
    message: str

    def __init__(self, _id: int) -> None:
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

    def init(self, _id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(id=_id)
        super().init(self.message)


class PriceAlreadyExists(BaseException):
    _ERROR_MESSAGE_TEMPLATE: Final[str] = "Цена для блюда с id '{dish_id}' уже существует"

    def init(self, dish_id: int) -> None:
        self.message = self._ERROR_MESSAGE_TEMPLATE.format(dish_id=dish_id)
        super().init(self.message)