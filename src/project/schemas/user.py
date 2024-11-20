from pydantic import BaseModel
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


class Client(ClientBase):
    clientid: int

    class Config:
        orm_mode = True