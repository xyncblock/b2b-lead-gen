from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
from urllib.parse import urlparse, urlunparse, quote

settings = get_settings()

# Fix DATABASE_URL - password starts with @ which breaks URL parsing
# We need to manually construct the URL with encoded password
db_url = settings.DATABASE_URL

# Handle the case where password starts with @
if "postgresql://" in db_url:
    # Extract components manually
    rest = db_url.replace("postgresql://", "")
    if "@" in rest:
        user_pass, host_db = rest.split("@", 1)
        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
            # URL-encode the password
            password = quote(password, safe="")
            db_url = f"postgresql://{user}:{password}@{host_db}"
        else:
            db_url = f"postgresql://{user_pass}@{host_db}"

# Also handle asyncpg prefix
db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")

engine = create_engine(
    db_url,
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