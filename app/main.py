from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text

from app import models, schemas, crud
from app.database import engine, SessionLocal, Base 

app = FastAPI(title="Contacts API")

# Створюємо таблиці (тільки один раз)
Base.metadata.create_all(bind=engine)

# Dependency для сесії
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception:
        raise HTTPException(status_code=500, detail="Error connecting to the database")


# CREATE
@app.post("/contacts/", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)


# READ
@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.get("/contacts/", response_model=list[schemas.ContactOut])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_contacts(db, skip=skip, limit=limit)


# UPDATE (PUT — повне оновлення)
@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact_full(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


# PATCH (часткове оновлення)
@app.patch("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact_partial(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact_partial(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact


# DELETE
@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_contact(db, contact_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": f"Contact {contact_id} deleted successfully"}


# Validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation Error",
            "errors": exc.errors(),
            "body": exc.body
        },
    )
