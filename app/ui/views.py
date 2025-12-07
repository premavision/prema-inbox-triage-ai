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

# Category label mappings
CATEGORY_LABELS = {
    "SALES_LEAD": "Sales Lead",
    "SUPPORT_REQUEST": "Support Request",
    "INTERNAL": "Internal",
    "OTHER": "Other",
}

CATEGORY_ICONS = {
    "SALES_LEAD": "💼",
    "SUPPORT_REQUEST": "🛟",
    "INTERNAL": "🏢",
    "OTHER": "📧",
}


def format_category_label(category: str | None) -> str:
    """Format category label for display."""
    if not category:
        return ""
    return CATEGORY_LABELS.get(category, category.replace("_", " ").title())


def get_category_icon(category: str | None) -> str:
    """Get icon for category."""
    if not category:
        return ""
    return CATEGORY_ICONS.get(category, "📧")


# Add custom filters to Jinja2 environment
templates.env.filters["format_category"] = format_category_label
templates.env.filters["category_icon"] = get_category_icon


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, repository: EmailRepository = Depends(deps.get_repository)) -> HTMLResponse:
    import time
    emails = repository.list_emails()
    error = request.query_params.get("error")
    # Add timestamp to prevent caching of static files in development
    timestamp = int(time.time())
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "emails": emails, 
        "error": error,
        "timestamp": timestamp
    })


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
