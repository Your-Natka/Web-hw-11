# crud.py
from sqlalchemy.orm import Session
from models import Contact
from schemas import ContactCreate, ContactUpdate
from typing import List, Optional
from datetime import date, datetime, timedelta

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        birthday=contact.birthday,
        extra=contact.extra
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()

def update_contact(db: Session, contact_id: int, data: ContactUpdate) -> Optional[Contact]:
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(db_contact, field, value)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> bool:
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return False
    db.delete(db_contact)
    db.commit()
    return True

def search_contacts(db: Session, q: str, skip: int = 0, limit: int = 100):
    # simple case-insensitive search for first_name, last_name or email
    like_q = f"%{q}%"
    return db.query(Contact).filter(
        (Contact.first_name.ilike(like_q)) |
        (Contact.last_name.ilike(like_q)) |
        (Contact.email.ilike(like_q))
    ).offset(skip).limit(limit).all()

def contacts_with_birthdays_next_days(db: Session, days: int = 7):
    """
    Return contacts that have birthday within next `days` days (from today),
    independent of year. We fetch candidates with non-null birthday and filter in Python.
    """
    today = date.today()
    end_date = today + timedelta(days=days)
    results = []
    all_with_bday = db.query(Contact).filter(Contact.birthday.isnot(None)).all()
    for c in all_with_bday:
        b = c.birthday
        # compute next occurrence in current year
        try:
            next_occurrence = date(today.year, b.month, b.day)
        except ValueError:
            # handle Feb 29 on non-leap years by treating as Feb 28
            next_occurrence = date(today.year, 2, 28)
        if next_occurrence < today:
            try:
                next_occurrence = date(today.year + 1, b.month, b.day)
            except ValueError:
                next_occurrence = date(today.year + 1, 2, 28)
        if today <= next_occurrence <= end_date:
            results.append((c, next_occurrence))
    # optionally sort by upcoming date
    results.sort(key=lambda tup: tup[1])
    # return only contacts
    return [t[0] for t in results]
