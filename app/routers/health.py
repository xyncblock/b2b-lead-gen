from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from datetime import datetime
import redis

from app.database import get_db
from app.config import get_settings
from app.schemas import HealthStatus, HealthReady

settings = get_settings()
router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
def health_live():
    return HealthStatus(
        status="alive",
        timestamp=datetime.utcnow()
    )


@router.get("/ready")
def health_ready(db: Session = Depends(get_db)):
    db_ok = False
    redis_ok = False
    
    # Check database
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        pass
    
    # Check Redis
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
        redis_ok = True
    except Exception:
        pass
    
    status = "ready" if (db_ok and redis_ok) else "not_ready"
    
    return HealthReady(
        database=db_ok,
        redis=redis_ok,
        status=status
    )
