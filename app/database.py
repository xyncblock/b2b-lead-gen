from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
from urllib.parse import urlparse, urlunparse, quote

settings = get_settings()

# Parse and fix DATABASE_URL to handle special characters in password
parsed = urlparse(settings.DATABASE_URL)
# Reconstruct with proper encoding
fixed_url = urlunparse(parsed)

# Use sync engine for Render compatibility
engine = create_engine(
    fixed_url.replace("postgresql+asyncpg://", "postgresql://"),
    echo=settings.DEBUG,
    future=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()