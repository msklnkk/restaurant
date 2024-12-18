from typing import Annotated
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from project.schemas.auth import TokenData
from project.schemas.user import ClientSchema
from project.core.config import settings
from project.core.exceptions import CredentialsException
from project.resource.auth import oauth2_scheme

from project.infrastructure.postgres.repository.client_repo import ClientRepository
from project.infrastructure.postgres.repository.dish_repo import DishRepository
from project.infrastructure.postgres.repository.order_repo import OrderRepository
from project.infrastructure.postgres.repository.staff_repo import StaffRepository
from project.infrastructure.postgres.repository.table_repo import TableRepository
from project.infrastructure.postgres.repository.orderedDish_repo import OrderedDishRepository
from project.infrastructure.postgres.repository.dishProducts_repo import DishProductsRepository
from project.infrastructure.postgres.repository.delivery_repo import DeliveryRepository
from project.infrastructure.postgres.repository.shelfLife_repo import ShelfLifeRepository
from project.infrastructure.postgres.repository.orderedDrink_repo import OrderedDrinkRepository
from project.infrastructure.postgres.repository.productInDelivery_repo import ProductInDeliveryRepository
from project.infrastructure.postgres.repository.supplier_repo import SupplierRepository
from project.infrastructure.postgres.repository.drink_repo import DrinkRepository
from project.infrastructure.postgres.repository.price_repo import PriceRepository
from project.infrastructure.postgres.repository.product_repo import ProductRepository

from project.infrastructure.postgres.database import PostgresDatabase


client_repo = ClientRepository()
drink_repo = DrinkRepository()
price_repo = PriceRepository()
product_repo = ProductRepository()
staff_repo = StaffRepository()
supplier_repo = SupplierRepository()
table_repo = TableRepository()
delivery_repo = DeliveryRepository()
dishProducts_repo = DishProductsRepository()
dish_repo = DishRepository()
order_repo = OrderRepository()
productInDelivery_repo = ProductInDeliveryRepository()
shelfLife_repo = ShelfLifeRepository()
orderedDish_repo = OrderedDishRepository()
orderedDrink_repo = OrderedDrinkRepository()
database = PostgresDatabase()



AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные для авторизации"
async def get_current_client(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_AUTH_KEY.get_secret_value(),
            algorithms=[settings.AUTH_ALGORITHM],
        )
        email: str = payload.get("sub")
        if email is None:
            raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
        token_data = TokenData(username=email)
    except JWTError:
        raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
    async with database.session() as session:
        client = await client_repo.get_user_by_mail(
            session=session,
            mail=token_data.username,
        )
    if client is None:
        raise CredentialsException(detail=AUTH_EXCEPTION_MESSAGE)
    return client

def check_for_admin_access(client: ClientSchema) -> None:
    if not client.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только админ имеет права добавлять/изменять/удалять данные"
        )
