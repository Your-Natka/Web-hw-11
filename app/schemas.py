from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional


# --- ITEMS ---
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True


# --- CONTACTS ---
class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    preferred_contact_method: Optional[str] = None  # email / sms
    sent: Optional[bool] = False
    birth_date: Optional[date] = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    sent: Optional[bool] = None
    birth_date: Optional[date] = None


class ContactOut(ContactBase):
    id: int

    class Config:
        from_attributes = True
