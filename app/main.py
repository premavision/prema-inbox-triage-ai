"""FastAPI application entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel

from app.api.routes import config, emails, health
from app.core.config import get_settings
from app.db.session import engine
from app.models import email  # noqa: F401 - Import to register models
from app.ui.views import router as ui_router

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.on_event("startup")
def on_startup() -> None:
    """Initialize database tables on startup."""
    SQLModel.metadata.create_all(engine)
    
    # Auto-seed data for demo purposes if DB is empty
    from app.seed_db import seed_emails
    try:
        seed_emails()
    except Exception as e:
        print(f"Error seeding database: {e}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(config.router)
app.include_router(emails.router)
app.include_router(ui_router)

app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")
templates = Jinja2Templates(directory="app/ui/templates")
