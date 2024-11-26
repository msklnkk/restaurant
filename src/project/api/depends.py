from project.infrastructure.postgres.repository.user_repo import ClientRepository, DrinkRepository
from project.infrastructure.postgres.database import PostgresDatabase


user_repo = ClientRepository()
drink_repo = DrinkRepository()
database = PostgresDatabase()
