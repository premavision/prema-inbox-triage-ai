from datetime import datetime
from typing import Any

import pytest

from app.models.email import Email
from app.providers.llm.base import ClassificationResult, LLMClient
from app.repositories.email_repository import EmailRepository
from app.services.classification_service import ClassificationService


class FakeLLM(LLMClient):
    async def classify_email(self, *, subject: str, body: str) -> ClassificationResult:  # type: ignore[override]
        return ClassificationResult(lead_flag=True, category="SALES_LEAD", priority="HIGH", entities={})

    async def generate_reply(self, *, subject: str, body: str, summary: str | None = None):  # pragma: no cover
        raise NotImplementedError


class FakeRepository(EmailRepository):
    def __init__(self) -> None:
        self.saved: dict[str, Any] = {}
        self.email = Email(
            id=1,
            provider_id="1",
            sender="a",
            recipients="b",
            subject="hi",
            snippet="",
            body="body",
            received_at=datetime.utcnow(),
        )

    def save_classification(self, email: Email, **kwargs: Any) -> Email:  # type: ignore[override]
        self.saved = kwargs
        return email

    def get(self, email_id: int) -> Email:  # type: ignore[override]
        return self.email


@pytest.mark.asyncio
async def test_classification_updates_fields() -> None:
    repo = FakeRepository()
    service = ClassificationService(repo, FakeLLM())

    email = await service.retriage(1)

    assert repo.saved["lead_flag"] is True
    assert email.subject == "hi"
