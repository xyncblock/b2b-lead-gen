from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, businesses, health

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# Static files and templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# API routers
app.include_router(auth.router)
app.include_router(businesses.router)
app.include_router(health.router)


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/businesses")
async def businesses_page(request: Request):
    return templates.TemplateResponse("businesses.html", {"request": request})
