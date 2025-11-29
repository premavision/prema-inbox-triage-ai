"""Provider configuration endpoint."""

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.providers import ProviderConfig, ProvidersResponse

router = APIRouter()


@router.get("/config/providers", response_model=ProvidersResponse)
def providers(settings: Settings = Depends(get_settings)) -> ProvidersResponse:
    providers = [
        ProviderConfig(
            name="gmail",
            enabled=settings.gmail_enabled,
            details={
                "user": settings.gmail_user_email or "not-set",
                "mode": "mock" if settings.gmail_use_mock else "real",
            },
        ),
        ProviderConfig(
            name=settings.llm_provider,
            enabled=bool(settings.openai_api_key),
            details={"model": settings.openai_model},
        ),
    ]
    return ProvidersResponse(providers=providers)
