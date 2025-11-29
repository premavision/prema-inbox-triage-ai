"""Schemas representing configured providers."""

from pydantic import BaseModel


class ProviderConfig(BaseModel):
    name: str
    enabled: bool
    details: dict[str, str] | None = None


class ProvidersResponse(BaseModel):
    providers: list[ProviderConfig]
