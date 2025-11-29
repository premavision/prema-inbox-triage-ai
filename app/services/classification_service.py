"""Classification and triage service."""

from __future__ import annotations

from app.models.email import Email
from app.providers.llm.base import LLMClient
from app.repositories.email_repository import EmailRepository


class ClassificationService:
    """Uses LLM to classify stored emails."""

    def __init__(self, repository: EmailRepository, llm_client: LLMClient) -> None:
        self.repository = repository
        self.llm_client = llm_client

    async def classify_email(self, email: Email) -> Email:
        result = await self.llm_client.classify_email(subject=email.subject, body=email.body)
        return self.repository.save_classification(
            email,
            lead_flag=result.lead_flag,
            category=result.category,
            priority=result.priority,
            entities=result.entities,
            status="classified",
        )

    async def retriage(self, email_id: int) -> Email:
        email = self.repository.get(email_id)
        return await self.classify_email(email)
