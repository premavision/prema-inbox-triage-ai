"""FastAPI dependency wiring."""

from collections.abc import AsyncGenerator

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.db.session import get_session
from app.providers.email.gmail import GmailProvider
from app.providers.llm.openai_client import OpenAILLMClient
from app.repositories.email_repository import EmailRepository
from app.services.classification_service import ClassificationService
from app.services.ingestion_service import IngestionService
from app.services.reply_service import ReplyService


async def get_db() -> AsyncGenerator:
    with get_session() as session:
        yield session


def get_repository(session=Depends(get_db)) -> EmailRepository:  # type: ignore[override]
    return EmailRepository(session)


def get_gmail_provider(settings: Settings = Depends(get_settings)) -> GmailProvider:
    return GmailProvider(settings)


def get_llm_client(settings: Settings = Depends(get_settings)) -> OpenAILLMClient:
    return OpenAILLMClient(settings)


def get_ingestion_service(
    repository: EmailRepository = Depends(get_repository),
    provider: GmailProvider = Depends(get_gmail_provider),
) -> IngestionService:
    return IngestionService(provider, repository)


def get_classification_service(
    repository: EmailRepository = Depends(get_repository),
    llm_client=Depends(get_llm_client),
) -> ClassificationService:
    return ClassificationService(repository, llm_client)


def get_reply_service(
    repository: EmailRepository = Depends(get_repository),
    llm_client=Depends(get_llm_client),
) -> ReplyService:
    return ReplyService(repository, llm_client)
