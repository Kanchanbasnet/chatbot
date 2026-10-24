import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

dotenv.load_dotenv()
import os

postgres_url = os.getenv("POSTGRES_URL")
if not postgres_url:
    raise RuntimeError("POSTGRES URL is not configured!!")

engine = create_engine(postgres_url)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass


    