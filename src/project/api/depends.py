from project.infrastructure.postgres.repository.user_repo import ClientRepository, DrinkRepository, PriceRepository
from project.infrastructure.postgres.database import PostgresDatabase


user_repo = ClientRepository()
drink_repo = DrinkRepository()
price_repo = PriceRepository()
database = PostgresDatabase()
