from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings
from urllib.parse import quote

settings = get_settings()

# Fix DATABASE_URL - password starts with @ which breaks URL parsing
db_url = settings.DATABASE_URL

# Handle the case where password starts with @
# URL format: postgresql://user:password@host:port/db
# When password starts with @, we need to encode it
if "postgresql://" in db_url:
    # Remove prefix
    rest = db_url.replace("postgresql://", "")
    # Find the LAST @ which separates credentials from host
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