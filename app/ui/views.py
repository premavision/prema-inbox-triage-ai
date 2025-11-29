"""Server-rendered UI views."""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api import deps
from app.repositories.email_repository import EmailRepository
from app.services.classification_service import ClassificationService
from app.services.reply_service import ReplyService

router = APIRouter()
templates = Jinja2Templates(directory="app/ui/templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, repository: EmailRepository = Depends(deps.get_repository)) -> HTMLResponse:
    emails = repository.list_emails()
    return templates.TemplateResponse("dashboard.html", {"request": request, "emails": emails})


@router.post("/emails/{email_id}/retriage")
async def retriage_email_ui(
    email_id: int,
    classification_service: ClassificationService = Depends(deps.get_classification_service),
    reply_service: ReplyService = Depends(deps.get_reply_service),
) -> RedirectResponse:
    """Retriage an email from UI."""
    try:
        email = await classification_service.retriage(email_id)
        await reply_service.ensure_reply(email)
    except ValueError:
        pass  # Email not found, redirect anyway
    return RedirectResponse(url="/", status_code=303)
