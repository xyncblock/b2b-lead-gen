from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - try to init database but don't fail if it doesn't work
    try:
        from app.database import engine, Base
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database error (non-fatal): {e}")
    yield
    # Shutdown
    try:
        from app.database import engine
        engine.dispose()
    except:
        pass


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Import routers after app creation
from app.routers import auth, businesses, health

# API routers
app.include_router(auth.router)
app.include_router(businesses.router)
app.include_router(health.router)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")


@app.get("/businesses")
async def businesses_page(request: Request):
    return templates.TemplateResponse(request, "businesses.html")