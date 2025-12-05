"""Email sending service."""

from __future__ import annotations

from app.models.email import Email
from app.providers.email.base import EmailProvider
from app.repositories.email_repository import EmailRepository


class SendService:
    """Service for sending email replies."""

    def __init__(self, provider: EmailProvider, repository: EmailRepository) -> None:
        self.provider = provider
        self.repository = repository

    def send_reply(self, email: Email, reply_body: str) -> bool:
        """Send a reply for an email."""
        # Extract recipient from original email
        to = email.sender
        
        # Prepare subject (add Re: if not present)
        subject = email.subject
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"
        
        # Send via provider
        success = self.provider.send_reply(
            to=to,
            subject=subject,
            body=reply_body,
            thread_id=email.thread_id,
        )
        
        if success:
            # Update email status
            self.repository.update_status(email, "reply_sent")
        
        return success




