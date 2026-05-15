from urllib.parse import urlparse, urlunparse, quote, unquote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
import logging
import traceback

logger = logging.getLogger(__name__)

settings = get_settings()

# Parse URL properly so we can handle special chars in password safely
parsed = urlparse(settings.DATABASE_URL)

# Rebuild netloc with decoded password (keep @ encoded so it doesn't break the URL)
username = unquote(parsed.username) if parsed.username else ""
password = unquote(parsed.password) if parsed.password else ""
# Re-encode @ and / in password so they don't break URL structure
safe_password = quote(password, safe="")

netloc = f"{quote(username, safe='')}:{safe_password}@{parsed.hostname}"
if parsed.port:
    netloc += f":{parsed.port}"

# Swap to sync driver and rebuild
db_url = urlunparse((
    "postgresql",
    netloc,
    parsed.path,
    parsed.params,
    parsed.query,
    parsed.fragment
))

# Add SSL mode for Supabase
if "supabase.co" in db_url and "?" not in db_url:
    db_url += "?sslmode=require"

# Mask password in logs
safe_log = db_url.replace(safe_password, "***")
logger.info(f"Database URL: {safe_log}")

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