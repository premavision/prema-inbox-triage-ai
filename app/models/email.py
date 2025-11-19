"""SQLModel entity for emails."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, JSON, SQLModel


class Email(SQLModel, table=True):
    """Normalized email data and classification results."""

    id: Optional[int] = Field(default=None, primary_key=True)
    provider_id: str
    thread_id: str | None = None
    sender: str
    recipients: str
    cc: str | None = None
    subject: str
    snippet: str | None = None
    body: str
    received_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    processing_status: str = Field(default="pending")

    lead_flag: bool = False
    category: str | None = None
    priority: str | None = None
    extracted_entities: dict | None = Field(default=None, sa_column=Column(JSON))

    suggested_reply: str | None = None
    reply_generated_at: datetime | None = Field(default=None, sa_column=Column(DateTime(timezone=True), nullable=True))
