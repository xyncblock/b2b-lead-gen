from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
import logging
import traceback

logger = logging.getLogger(__name__)

settings = get_settings()

# Use DATABASE_URL as-is, just add SSL for Supabase
db_url = settings.DATABASE_URL

# Replace asyncpg prefix if present
db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

# Add SSL mode for Supabase
if "supabase.co" in db_url and "?" not in db_url:
    db_url += "?sslmode=require"

logger.info(f"Database URL: {db_url}")

try:
    engine = create_engine(
        db_url,
        echo=settings.DEBUG,
        future=True
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    logger.error(traceback.format_exc())
    # Fallback - this will fail but app will start
    engine = create_engine("postgresql://localhost:5432/dummy", echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()