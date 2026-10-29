import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DatabaseUrl = os.getenv("DATABASE_URL")

if not DatabaseUrl:
    raise RuntimeError("DATABASE_URL is missing from .env")


engine = create_engine(DatabaseUrl)

SessionLocal = sessionmaker(
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)



class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()