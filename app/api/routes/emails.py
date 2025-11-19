"""Email API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query

from app.api import deps
from app.repositories.email_repository import EmailRepository
from app.schemas.email import EmailListResponse, EmailSchema, EmailSyncResponse, ReTriageResponse
from app.services.classification_service import ClassificationService
from app.services.ingestion_service import IngestionService
from app.services.reply_service import ReplyService

router = APIRouter(prefix="/emails")


@router.post("/sync", response_model=EmailSyncResponse)
def sync_emails(
    service: IngestionService = Depends(deps.get_ingestion_service),
) -> EmailSyncResponse:
    result = service.sync_recent()
    return EmailSyncResponse(synced=result.synced)


@router.get("", response_model=EmailListResponse)
def list_emails(
    repository: EmailRepository = Depends(deps.get_repository),
    is_lead: bool | None = Query(default=None),
    category: str | None = Query(default=None),
    priority: str | None = Query(default=None),
) -> EmailListResponse:
    emails = repository.list_emails(is_lead=is_lead, category=category, priority=priority)
    return EmailListResponse(emails=[EmailSchema.model_validate(email) for email in emails])


@router.get("/{email_id}", response_model=EmailSchema)
def get_email(email_id: int, repository: EmailRepository = Depends(deps.get_repository)) -> EmailSchema:
    try:
        email = repository.get(email_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return EmailSchema.model_validate(email)


@router.post("/{email_id}/retriage", response_model=ReTriageResponse)
async def retriage_email(
    email_id: int,
    classification_service: ClassificationService = Depends(deps.get_classification_service),
    reply_service: ReplyService = Depends(deps.get_reply_service),
) -> ReTriageResponse:
    try:
        email = await classification_service.retriage(email_id)
        await reply_service.ensure_reply(email)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return ReTriageResponse(email=EmailSchema.model_validate(email))
