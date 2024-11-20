from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey

from project.infrastructure.postgres.database import Base


class Client(Base):
    __tablename__ = "clients"

    clientid = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    mail = Column(String)
    discount_percentage = Column(Integer)