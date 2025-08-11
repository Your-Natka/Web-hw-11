from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    first_name: str = Field(..., example="Іван")
    last_name: str = Field(..., example="Іваненко")
    email: EmailStr
    phone: Optional[str] = Field(None, example="+380123456789")
    birthday: Optional[date] = Field(None, example="1990-05-20")
    extra: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    birthday: Optional[date]
    extra: Optional[str]

class ContactOut(ContactBase):
    id: int

    class Config:
        orm_mode = True
