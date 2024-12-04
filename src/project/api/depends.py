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
