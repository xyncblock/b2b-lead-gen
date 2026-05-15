from urllib.parse import unquote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings

settings = get_settings()

# Decode URL-encoded chars (e.g. %40 -> @, %24 -> $) then swap to sync driver
sync_url = unquote(settings.DATABASE_URL).replace("postgresql+asyncpg://", "postgresql://")

engine = create_engine(sync_url, echo=settings.DEBUG, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
