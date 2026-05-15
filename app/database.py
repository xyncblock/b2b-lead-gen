from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
from urllib.parse import unquote, quote
import logging

logger = logging.getLogger(__name__)

settings = get_settings()

# Fix DATABASE_URL - handle already encoded URLs
db_url = settings.DATABASE_URL

# First unquote any existing encoding, then re-quote properly
db_url = unquote(db_url)

# Handle the case where password starts with @
if "postgresql://" in db_url:
    rest = db_url.replace("postgresql://", "")
    if "@" in rest:
        # Split from the right to handle @ in password
        user_pass, host_db = rest.rsplit("@", 1)
        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
            # URL-encode special characters in password
            password = quote(password, safe="")
            db_url = f"postgresql://{user}:{password}@{host_db}"
        else:
            db_url = f"postgresql://{user_pass}@{host_db}"

# Also handle asyncpg prefix
db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

# Add SSL mode for Supabase
if "supabase.co" in db_url and "?" not in db_url:
    db_url += "?sslmode=require"

logger.info(f"Database URL (masked): postgresql://*****@{db_url.split(@)[1] if @ in db_url else unknown}")

try:
    engine = create_engine(
        db_url,
        echo=settings.DEBUG,
        future=True
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    # Create a dummy engine for startup
    engine = create_engine("postgresql://localhost:5432/dummy", echo=False, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()