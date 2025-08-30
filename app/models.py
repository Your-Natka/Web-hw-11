from sqlalchemy import Column, Integer, String, Boolean, Date
from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    preferred_contact_method = Column(String, index=True)  # email / sms
    sent = Column(Boolean, default=False)
    birth_date = Column(Date)  # для пошуку днів народження

