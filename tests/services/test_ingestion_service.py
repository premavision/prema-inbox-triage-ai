from datetime import datetime

from datetime import datetime

from app.providers.email.base import EmailMessage
from app.repositories.email_repository import EmailRepository
from app.services.ingestion_service import IngestionService


class FakeProvider:
    def list_recent_messages(self, *, limit: int = 10):
        for idx in range(limit):
            yield EmailMessage(
                provider_id=str(idx),
                thread_id=None,
                sender="from@example.com",
                recipients=["to@example.com"],
                cc=[],
                subject="Hi",
                snippet="Snippet",
                body="Body",
                received_at=datetime.utcnow(),
            )


class FakeRepository(EmailRepository):
    def __init__(self) -> None:
        self.created = 0

    def create_email(self, **kwargs):  # type: ignore[override]
        self.created += 1
        return kwargs


def test_sync_recent_counts_inserted() -> None:
    repo = FakeRepository()
    service = IngestionService(FakeProvider(), repo)

    result = service.sync_recent(limit=3)

    assert repo.created == 3
    assert result.synced == 3
