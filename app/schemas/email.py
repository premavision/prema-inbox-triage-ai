"""Pydantic models for API responses."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class EmailSchema(BaseModel):
    id: int
    provider_id: str
    thread_id: str | None
    sender: str
    recipients: str
    cc: str | None
    subject: str
    snippet: str | None
    body: str
    received_at: datetime
    processing_status: str
    lead_flag: bool
    category: str | None
    priority: str | None
    extracted_entities: Optional[dict[str, Any]]
    suggested_reply: str | None
    reply_generated_at: datetime | None

    class Config:
        from_attributes = True


class EmailListResponse(BaseModel):
    emails: list[EmailSchema]


class EmailSyncResponse(BaseModel):
    synced: int


class ReTriageResponse(BaseModel):
    email: EmailSchema
