"""Gmail provider stub implementation."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from app.core.config import Settings
from app.providers.email.base import EmailMessage, EmailProvider


class GmailProvider:
    """Simplified Gmail provider used for demos and tests."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def name(self) -> str:
        return "gmail"

    def is_configured(self) -> bool:
        return bool(
            self.settings.gmail_client_id
            and self.settings.gmail_client_secret
            and self.settings.gmail_refresh_token
            and self.settings.gmail_user_email
        )

    def list_recent_messages(self, *, limit: int = 10) -> Iterable[EmailMessage]:
        # TODO: integrate with Gmail REST API using google-api-python-client
        # For now, return mocked data to unblock demo/testing
        now = datetime.now(tz=timezone.utc)
        for idx in range(limit):
            yield EmailMessage(
                provider_id=f"mock-{idx}",
                thread_id=f"thread-{idx}",
                sender="prospect@example.com",
                recipients=[self.settings.gmail_user_email or "triage@example.com"],
                cc=[],
                subject=f"Demo inquiry #{idx}",
                snippet="Interested in automation services",
                body=("Hello, we would like to learn more about your AI automation offerings."),
                received_at=now,
            )
