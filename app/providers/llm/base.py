"""LLM client abstractions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass
class ClassificationResult:
    lead_flag: bool
    category: str
    priority: str
    entities: dict | None


@dataclass
class ReplyResult:
    body: str


class LLMClient(Protocol):
    """Interface describing interactions with text generation models."""

    async def classify_email(self, *, subject: str, body: str) -> ClassificationResult:
        ...

    async def generate_reply(
        self,
        *,
        subject: str,
        body: str,
        summary: str | None = None,
    ) -> ReplyResult:
        ...
