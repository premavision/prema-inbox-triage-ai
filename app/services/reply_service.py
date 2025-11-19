"""Suggested reply generation."""

from __future__ import annotations

from app.models.email import Email
from app.providers.llm.base import LLMClient
from app.repositories.email_repository import EmailRepository


class ReplyService:
    """Generates reply drafts for important emails."""

    def __init__(self, repository: EmailRepository, llm_client: LLMClient) -> None:
        self.repository = repository
        self.llm_client = llm_client

    async def ensure_reply(self, email: Email) -> Email:
        if not email.lead_flag and email.priority not in {"HIGH", "MEDIUM"}:
            self.repository.update_status(email, "no_reply_needed")
            return email
        reply = await self.llm_client.generate_reply(subject=email.subject, body=email.body)
        self.repository.save_reply(email, reply.body)
        self.repository.update_status(email, "reply_generated")
        return email
