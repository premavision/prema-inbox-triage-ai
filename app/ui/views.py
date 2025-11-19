"""Server-rendered UI views."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api import deps
from app.repositories.email_repository import EmailRepository

router = APIRouter()
templates = Jinja2Templates(directory="app/ui/templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, repository: EmailRepository = Depends(deps.get_repository)) -> HTMLResponse:
    emails = repository.list_emails()
    return templates.TemplateResponse("dashboard.html", {"request": request, "emails": emails})
