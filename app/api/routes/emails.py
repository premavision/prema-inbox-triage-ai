"""Email API endpoints."""

from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import RedirectResponse, Response, JSONResponse

from app.api import deps
from app.providers.email.gmail import GmailProvider
from app.repositories.email_repository import EmailRepository
from app.schemas.email import EmailListResponse, EmailSchema, EmailSyncResponse, ReTriageResponse
from app.services.classification_service import ClassificationService
from app.services.ingestion_service import IngestionService
from app.services.reply_service import ReplyService
from app.services.send_service import SendService

router = APIRouter(prefix="/emails")


@router.post("/sync", response_model=None)
async def sync_emails(
    request: Request,
    service: IngestionService = Depends(deps.get_ingestion_service),
    repository: EmailRepository = Depends(deps.get_repository),
    llm_client=Depends(deps.get_llm_client),
    provider: GmailProvider = Depends(deps.get_gmail_provider),
    simulate_error: bool = Query(default=False),
) -> Response:
    """Sync emails, classify them, and generate replies. Returns JSON for API calls or redirects for form submissions."""
    # Set error simulation if requested
    if simulate_error:
        provider.set_simulate_error(True)
    
    try:
        result = service.sync_recent()
        
        # Use the same repository for all operations to avoid session conflicts
        # Create services with the shared repository
        classification_service = ClassificationService(repository, llm_client)
        reply_service = ReplyService(repository, llm_client)
        
        # Automatically classify and generate replies for unclassified emails
        # Only process newly synced emails to speed up the process
        all_emails = repository.list_emails()
        # Get only the most recent unclassified emails (limit to last 5 for speed)
        unclassified = [e for e in all_emails if not e.category][:5]
        
        classified_count = 0
        reply_count = 0
        
        # Process emails sequentially but quickly (classification happens in background)
        for email in unclassified:
            try:
                email = await classification_service.classify_email(email)
                classified_count += 1
                email = await reply_service.ensure_reply(email)
                if email.suggested_reply:
                    reply_count += 1
            except Exception as e:
                # Log error but continue with other emails
                print(f"Error processing email {email.id}: {e}")
        
        # Check if this is a form submission (browser request)
        content_type = request.headers.get("content-type", "")
        accept = request.headers.get("accept", "")
        is_form = "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type
        wants_json = "application/json" in accept
        
        if is_form and not wants_json:
            return RedirectResponse(url="/", status_code=303)
        return JSONResponse(content={
            "success": True,
            "synced": result.synced,
            "classified": classified_count,
            "replies_generated": reply_count
        })
    except Exception as e:
        # Reset error flag
        provider.set_simulate_error(False)
        
        # Log the full error for debugging
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in sync_emails: {error_traceback}")
        
        # Check if this is a form submission (browser request)
        content_type = request.headers.get("content-type", "")
        accept = request.headers.get("accept", "")
        is_form = "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type
        wants_json = "application/json" in accept
        
        error_message = str(e)
        if is_form and not wants_json:
            # For form submissions, redirect with error in query param
            return RedirectResponse(url=f"/?error={error_message}", status_code=303)
        # For API calls, return JSON error
        return JSONResponse(
            content={"success": False, "error": error_message},
            status_code=500
        )
    finally:
        # Always reset error flag
        provider.set_simulate_error(False)


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


@router.post("/{email_id}/generate-reply", response_model=EmailSchema)
async def generate_reply_draft(
    email_id: int,
    repository: EmailRepository = Depends(deps.get_repository),
    reply_service: ReplyService = Depends(deps.get_reply_service),
) -> EmailSchema:
    try:
        email = repository.get(email_id)
        email = await reply_service.create_draft_reply(email)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return EmailSchema.model_validate(email)


@router.delete("/reset")
@router.post("/reset")
async def reset_emails(
    request: Request,
    repository: EmailRepository = Depends(deps.get_repository),
    provider: GmailProvider = Depends(deps.get_gmail_provider),
) -> Response:
    """Reset all emails and mock counter. Returns JSON for API calls or redirects for form submissions."""
    try:
        deleted_count = repository.delete_all()
        provider.reset_mock_counter()
        
        # Check if this is a form submission (browser request)
        content_type = request.headers.get("content-type", "")
        accept = request.headers.get("accept", "")
        is_form = "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type
        wants_json = "application/json" in accept
        
        if wants_json or not is_form:
            return JSONResponse(content={"success": True, "deleted": deleted_count})
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        error_message = str(e)
        content_type = request.headers.get("content-type", "")
        accept = request.headers.get("accept", "")
        is_form = "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type
        wants_json = "application/json" in accept
        
        if wants_json or not is_form:
            return JSONResponse(
                content={"success": False, "error": error_message},
                status_code=500
            )
        return RedirectResponse(url=f"/?error={error_message}", status_code=303)


@router.post("/{email_id}/send")
def send_reply(
    email_id: int,
    request: Request,
    repository: EmailRepository = Depends(deps.get_repository),
    send_service: SendService = Depends(deps.get_send_service),
    reply_body: str | None = Form(default=None),
) -> Response:
    """Send a reply email."""
    try:
        email = repository.get(email_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    
    # Get reply body from form or use suggested_reply
    if not reply_body and not email.suggested_reply:
        raise HTTPException(status_code=400, detail="No reply body provided and no suggested reply available.")
    
    # Use form reply_body if provided, otherwise use suggested_reply
    body_to_send = reply_body if reply_body else email.suggested_reply
    
    if not body_to_send:
        raise HTTPException(status_code=400, detail="No reply body available.")
    
    # Send the reply
    success = send_service.send_reply(email, body_to_send)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send reply. Check logs for details.")
    
    # Check if this is a form submission (browser request)
    content_type = request.headers.get("content-type", "")
    accept = request.headers.get("accept", "")
    
    is_form = "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type
    wants_json = "application/json" in accept
    
    if is_form and not wants_json:
        return RedirectResponse(url="/", status_code=303)
    
    return JSONResponse(content={"success": True, "message": "Reply sent successfully"})
