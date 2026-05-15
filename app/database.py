from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
import logging
import traceback
import ssl

logger = logging.getLogger(__name__)

settings = get_settings()

# Use DATABASE_URL as-is, just swap asyncpg to sync if needed
db_url = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

# Strip query params for connect_args handling
from urllib.parse import urlparse, urlunparse
parsed = urlparse(db_url)
base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

logger.info(f"Database URL: {base_url.replace('://', '://***:***@')}")

try:
    engine = create_engine(
        base_url,
        echo=settings.DEBUG,
        future=True,
        connect_args={
            "sslmode": "require",
            "sslrootcert": "/etc/ssl/certs/ca-certificates.crt"
        }
    )
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
