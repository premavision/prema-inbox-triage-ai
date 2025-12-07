"""Email ingestion workflows."""

from __future__ import annotations

from dataclasses import dataclass

from app.providers.email.base import EmailProvider
from app.repositories.email_repository import EmailRepository


@dataclass
class IngestionResult:
    synced: int
    classified: int = 0
    replies_generated: int = 0


class IngestionService:
    """Service fetching emails from providers and persisting them."""

    def __init__(self, provider: EmailProvider, repository: EmailRepository) -> None:
        self.provider = provider
        self.repository = repository

    def sync_recent(self, *, limit: int = 5) -> IngestionResult:
        from app.models.email import Email
        from datetime import datetime
        
        emails = []
        for message in self.provider.list_recent_messages(limit=limit):
            emails.append(
                Email(
                    provider_id=message.provider_id,
                    sender=message.sender,
                    recipients=",".join(message.recipients),
                    subject=message.subject,
                    snippet=message.snippet,
                    body=message.body,
                    received_at=message.received_at,
                    thread_id=message.thread_id,
                    cc=",".join(message.cc) if message.cc else None,
                )
            )
        self.repository.upsert_emails(emails)
        return IngestionResult(synced=len(emails))
