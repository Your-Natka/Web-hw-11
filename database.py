from sqlalchemy import create_engine
> from sqlalchemy.orm import sessionmaker, declarative_base
> import os
> 
> DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/contacts_db")
> 
> engine = create_engine(DATABASE_URL, pool_pre_ping=True)
> SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
> Base = declarative_base()
> 
> # Dependency for FastAPI
> def get_db():
>     db = SessionLocal()
>     try:
>         yield db
>     finally:
>         db.close()
