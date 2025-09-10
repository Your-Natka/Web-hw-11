from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# --- ITEMS ---
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# --- CONTACTS ---
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    preferred_contact_method: Optional[str] = "email"
    sent: Optional[bool] = False
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactCreate(ContactBase):
    pass  # все вже є в ContactBase


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    sent: Optional[bool] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactOut(ContactBase):
    id: int

    model_config = {
        "from_attributes": True
    }
