from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, Base, get_db

# створюємо таблиці (для dev, у продакшн — alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Contacts API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.post("/contacts/", response_model=schemas.ContactOut, status_code=201)
def create_contact(contact_in: schemas.ContactCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Contact).filter(models.Contact.email == contact_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Contact with this email already exists")
    return crud.create_contact(db, contact_in)

@app.get("/contacts/", response_model=List[schemas.ContactOut])
def list_contacts(
    skip: int = 0,
    limit: int = 100,
    q: str = Query(None, description="Search query for first_name, last_name or email"),
    db: Session = Depends(get_db)
):
    if q:
        return crud.search_contacts(db, q, skip=skip, limit=limit)
    return crud.get_contacts(db, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    c = crud.get_contact(db, contact_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contact not found")
    return c

@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, contact_in: schemas.ContactUpdate, db: Session = Depends(get_db)):
    c = crud.update_contact(db, contact_id, contact_in)
    if not c:
        raise HTTPException(status_code=404, detail="Contact not found")
    return c

@app.delete("/contacts/{contact_id}", status_code=204)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_contact(db, contact_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Contact not found")
    return

@app.get("/birthdays/next7", response_model=List[schemas.ContactOut])
def birthdays_next_7_days(db: Session = Depends(get_db)):
    return crud.contacts_with_birthdays_next_days(db, days=7)
