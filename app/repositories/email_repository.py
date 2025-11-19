"""Data access helpers for emails."""

from collections.abc import Sequence
from datetime import datetime
from typing import Iterable, Optional

from sqlmodel import Session, select

from app.models.email import Email


class EmailRepository:
    """Encapsulates CRUD logic for email entities."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_emails(self, emails: Iterable[Email]) -> None:
        for email in emails:
            existing = self.session.exec(
                select(Email).where(Email.provider_id == email.provider_id)
            ).first()
            if existing:
                for field, value in email.model_dump().items():
                    setattr(existing, field, value)
            else:
                self.session.add(email)
        self.session.commit()

    def list_emails(
        self,
        is_lead: Optional[bool] = None,
        category: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Sequence[Email]:
        query = select(Email)
        if is_lead is not None:
            query = query.where(Email.lead_flag == is_lead)
        if category:
            query = query.where(Email.category == category)
        if priority:
            query = query.where(Email.priority == priority)
        query = query.order_by(Email.received_at.desc())
        return tuple(self.session.exec(query).all())

    def get(self, email_id: int) -> Email:
        email = self.session.get(Email, email_id)
        if not email:
            raise ValueError(f"Email {email_id} not found")
        return email

    def save_classification(
        self,
        email: Email,
        *,
        lead_flag: bool,
        category: str,
        priority: str,
        entities: dict | None,
        status: str,
    ) -> Email:
        email.lead_flag = lead_flag
        email.category = category
        email.priority = priority
        email.extracted_entities = entities
        email.processing_status = status
        self.session.add(email)
        self.session.commit()
        self.session.refresh(email)
        return email

    def save_reply(self, email: Email, body: str) -> Email:
        email.suggested_reply = body
        email.reply_generated_at = datetime.utcnow()
        self.session.add(email)
        self.session.commit()
        self.session.refresh(email)
        return email

    def update_status(self, email: Email, status: str) -> Email:
        email.processing_status = status
        self.session.add(email)
        self.session.commit()
        self.session.refresh(email)
        return email

    def find_by_provider_ids(self, provider_ids: Iterable[str]) -> dict[str, Email]:
        query = select(Email).where(Email.provider_id.in_(provider_ids))
        emails = self.session.exec(query).all()
        return {email.provider_id: email for email in emails}

    def create_email(
        self,
        *,
        provider_id: str,
        sender: str,
        recipients: str,
        subject: str,
        snippet: str,
        body: str,
        received_at: datetime,
        thread_id: str | None = None,
        cc: str | None = None,
    ) -> Email:
        email = Email(
            provider_id=provider_id,
            sender=sender,
            recipients=recipients,
            subject=subject,
            snippet=snippet,
            body=body,
            received_at=received_at,
            thread_id=thread_id,
            cc=cc,
        )
        self.session.add(email)
        self.session.commit()
        self.session.refresh(email)
        return email
