from project.infrastructure.postgres.repository.user_repo import ClientRepository, DrinkRepository, PriceRepository, ProductRepository
from project.infrastructure.postgres.repository.user_repo import StaffRepository, SupplierRepository, TableRepository, DeliveryRepository
from project.infrastructure.postgres.repository.user_repo import DishProductsRepository, DishRepository, OrderRepository, ProductInDeliveryRepository
from project.infrastructure.postgres.repository.user_repo import ShelfLifeRepository, OrderedDishRepository, OrderedDrinkRepository

from project.infrastructure.postgres.database import PostgresDatabase


user_repo = ClientRepository()
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
