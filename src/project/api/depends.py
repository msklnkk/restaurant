from project.infrastructure.postgres.repository.user_repo import ClientRepository
from project.infrastructure.postgres.database import PostgresDatabase


user_repo = ClientRepository()
database = PostgresDatabase()
