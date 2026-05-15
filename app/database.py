from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
import logging
import traceback

logger = logging.getLogger(__name__)

settings = get_settings()

# Use DATABASE_URL as-is, just swap asyncpg to sync if needed
db_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

logger.info(f"Database URL: {db_url.replace('://', '://***:***@')}")

try:
    engine = create_engine(db_url, echo=settings.DEBUG, future=True)
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    logger.error(traceback.format_exc())
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
