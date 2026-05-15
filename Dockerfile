FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Create tables and run
CMD ["sh", "-c", "python -c 'from app.database import Base, engine; Base.metadata.create_all(bind=engine)' && python -c 'from app.database import SessionLocal; from app.models import User; from app.auth import get_password_hash; db=SessionLocal(); db.add(User(email=\"rajithlbandara@gmail.com\", hashed_password=get_password_hash(\"11114444%%\"), is_active=True, is_superuser=True)); db.commit(); db.close()' 2>/dev/null || true && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
