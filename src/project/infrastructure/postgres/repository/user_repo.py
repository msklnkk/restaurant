from typing import Type
from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from project.schemas.user import ClientBase, ClientCreate, Client
from project.infrastructure.postgres.models import Client

from project.core.exceptions import UserNotFound, UserAlreadyExists


class ClientRepository:
    @staticmethod
    def get_client(db: Session, client_id: int):
        return db.query(Client).filter(Client.clientid == client_id).first()

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Client).offset(skip).limit(limit).all()

    @staticmethod
    def create_client(db: Session, client: ClientCreate):
        db_client = Client(**client.dict())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    @staticmethod
    def update_client(db: Session, client_id: int, client: ClientCreate):
        db_client = db.query(Client).filter(Client.clientid == client_id).first()
        if db_client:
            for key, value in client.dict().items():
                setattr(db_client, key, value)
            db.commit()
            db.refresh(db_client)
        return db_client

    @staticmethod
    def delete_client(db: Session, client_id: int):
        db_client = db.query(Client).filter(Client.clientid == client_id).first()
        if db_client:
            db.delete(db_client)
            db.commit()
            return True
        return False