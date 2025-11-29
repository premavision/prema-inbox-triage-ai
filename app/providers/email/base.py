"""Email provider abstraction."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Protocol


@dataclass
class EmailMessage:
    provider_id: str
    thread_id: str | None
    sender: str
    recipients: list[str]
    cc: list[str]
    subject: str
    snippet: str
    body: str
    received_at: datetime


class EmailProvider(Protocol):
    """Interface implemented by inbox providers (Gmail, Outlook, etc.)."""

    def list_recent_messages(self, *, limit: int = 10) -> Iterable[EmailMessage]:
        """Return recent messages metadata and body."""

    def name(self) -> str:
        """Display name used in provider status endpoints."""

    def is_configured(self) -> bool:
        """Return whether provider has enough credentials to operate."""
    
    def send_reply(self, *, to: str, subject: str, body: str, thread_id: str | None = None) -> bool:
        """Send a reply email. Returns True if successful, False otherwise."""