# app/database.py
from sqlmodel import create_engine, Session
from app.config import settings

# echo=True لعرض استعلامات SQL أثناء التطوير
engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
