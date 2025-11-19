"""OpenAI-based LLM client implementation."""

from __future__ import annotations

from textwrap import dedent

from openai import AsyncOpenAI

from app.core.config import Settings
from app.providers.llm.base import ClassificationResult, LLMClient, ReplyResult


class OpenAILLMClient(LLMClient):
    """LLM client that leverages OpenAI responses."""

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required for OpenAI client")
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def classify_email(self, *, subject: str, body: str) -> ClassificationResult:
        prompt = dedent(
            f"""
            You are an inbox triage assistant. Read the email below and return a JSON object with:
            - lead_flag (true/false)
            - category (one of SALES_LEAD, SUPPORT_REQUEST, INTERNAL, OTHER)
            - priority (HIGH, MEDIUM, LOW)
            - entities (sender_role, company if present)

            Subject: {subject}
            Body: {body}
            """
        )
        response = await self.client.responses.create(
            model=self.model,
            input=prompt,
            response_format={"type": "json_object"},
        )
        content = response.output[0].content[0].text  # type: ignore[index]
        data = self.client._parse_json(content)  # type: ignore[attr-defined]
        return ClassificationResult(
            lead_flag=bool(data.get("lead_flag")),
            category=str(data.get("category", "OTHER")),
            priority=str(data.get("priority", "LOW")),
            entities=data.get("entities"),
        )

    async def generate_reply(self, *, subject: str, body: str, summary: str | None = None) -> ReplyResult:
        prompt = dedent(
            f"""
            You craft short, friendly first-response emails. Include greeting, summary, 1-2 clarification
            questions, and a polite closing. Do not exceed 180 words.
            Subject: {subject}
            Body: {body}
            Summary/context: {summary or 'N/A'}
            """
        )
        response = await self.client.responses.create(model=self.model, input=prompt)
        text = response.output[0].content[0].text  # type: ignore[index]
        return ReplyResult(body=text.strip())
