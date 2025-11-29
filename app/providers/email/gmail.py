"""Gmail provider implementation with real API integration."""

from __future__ import annotations

import base64
import logging
from datetime import datetime, timezone
from typing import Iterable

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from app.core.config import Settings
from app.providers.email.base import EmailMessage, EmailProvider

# Gmail API scopes
# Include send scope for replying to emails
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

logger = logging.getLogger(__name__)


class GmailProvider:
    """Gmail provider with real API integration using OAuth2."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._service = None

    def name(self) -> str:
        return "gmail"

    def is_configured(self) -> bool:
        return bool(
            self.settings.gmail_client_id
            and self.settings.gmail_client_secret
            and self.settings.gmail_refresh_token
            and self.settings.gmail_user_email
        )

    def _get_credentials(self) -> Credentials | None:
        """Get OAuth2 credentials from refresh token."""
        if not self.is_configured():
            logger.debug("Gmail not configured - missing credentials")
            return None

        try:
            logger.debug("Creating Gmail credentials from refresh token")
            creds = Credentials(
                token=None,
                refresh_token=self.settings.gmail_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.settings.gmail_client_id,
                client_secret=self.settings.gmail_client_secret,
                scopes=SCOPES,
            )
            # Refresh the token if needed
            if not creds.valid:
                try:
                    logger.debug("Refreshing Gmail access token")
                    creds.refresh(Request())
                    logger.info("Gmail access token refreshed successfully")
                except Exception as e:
                    logger.error(f"Failed to refresh Gmail token: {type(e).__name__}: {e}")
                    return None
            else:
                logger.debug("Gmail credentials are valid")
            return creds
        except Exception as e:
            logger.error(f"Failed to create Gmail credentials: {type(e).__name__}: {e}")
            return None

    def _get_service(self):
        """Get Gmail API service instance."""
        if self._service is None:
            creds = self._get_credentials()
            if not creds:
                logger.debug("No credentials available, cannot create Gmail service")
                return None
            try:
                logger.debug("Building Gmail API service")
                self._service = build("gmail", "v1", credentials=creds)
                logger.info("Gmail API service created successfully")
            except Exception as e:
                logger.error(f"Failed to build Gmail service: {type(e).__name__}: {e}")
                return None
        return self._service

    def _parse_email_message(self, msg_id: str, msg_data: dict) -> EmailMessage | None:
        """Parse Gmail API message into EmailMessage."""
        try:
            headers = {h["name"].lower(): h["value"] for h in msg_data.get("payload", {}).get("headers", [])}

            # Extract email fields
            subject = headers.get("subject", "")
            sender = headers.get("from", "")
            to_header = headers.get("to", "")
            cc_header = headers.get("cc", "")
            date_str = headers.get("date", "")

            # Parse recipients
            recipients = [addr.strip() for addr in to_header.split(",")] if to_header else []
            cc = [addr.strip() for addr in cc_header.split(",")] if cc_header else []

            # Parse date
            try:
                from email.utils import parsedate_to_datetime

                received_at = parsedate_to_datetime(date_str) if date_str else datetime.now(tz=timezone.utc)
                if received_at.tzinfo is None:
                    received_at = received_at.replace(tzinfo=timezone.utc)
            except Exception:
                received_at = datetime.now(tz=timezone.utc)

            # Extract body
            body = ""
            snippet = msg_data.get("snippet", "")
            payload = msg_data.get("payload", {})
            parts = payload.get("parts", [])

            if not parts:
                # Simple message without parts
                body_data = payload.get("body", {}).get("data")
                if body_data:
                    body = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
            else:
                # Multipart message
                for part in parts:
                    mime_type = part.get("mimeType", "")
                    if mime_type == "text/plain":
                        body_data = part.get("body", {}).get("data")
                        if body_data:
                            body = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
                            break
                    elif mime_type == "text/html" and not body:
                        # Fallback to HTML if no plain text
                        body_data = part.get("body", {}).get("data")
                        if body_data:
                            body = base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")

            # Get thread ID
            thread_id = msg_data.get("threadId", "")

            return EmailMessage(
                provider_id=msg_id,
                thread_id=thread_id,
                sender=sender,
                recipients=recipients,
                cc=cc,
                subject=subject,
                snippet=snippet,
                body=body,
                received_at=received_at,
            )
        except Exception:
            return None

    def list_recent_messages(self, *, limit: int = 10) -> Iterable[EmailMessage]:
        """Fetch recent messages from Gmail API or return mock data."""
        # Check if mock mode is enabled (default)
        if self.settings.gmail_use_mock:
            logger.debug("Mock mode enabled, using mock email data")
            yield from self._get_mock_messages(limit=limit)
            return

        # Try to use real Gmail API if configured and mock is disabled
        try:
            if self.is_configured():
                logger.info(f"Attempting to fetch {limit} messages from Gmail API")
                service = self._get_service()
                if service:
                    try:
                        # List messages
                        logger.debug("Calling Gmail API to list messages")
                        results = (
                            service.users()
                            .messages()
                            .list(userId="me", maxResults=limit, q="is:inbox")
                            .execute()
                        )
                        messages = results.get("messages", [])
                        logger.info(f"Gmail API returned {len(messages)} message(s)")

                        for msg_ref in messages:
                            msg_id = msg_ref["id"]
                            try:
                                # Get full message details
                                logger.debug(f"Fetching full details for message {msg_id}")
                                msg = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
                                email_msg = self._parse_email_message(msg_id, msg)
                                if email_msg:
                                    logger.debug(f"Successfully parsed message: {email_msg.subject}")
                                    yield email_msg
                            except Exception as e:
                                logger.warning(f"Failed to parse message {msg_id}: {type(e).__name__}: {e}")
                                continue
                        logger.info("Successfully fetched messages from Gmail API")
                        return
                    except HttpError as e:
                        logger.error(f"Gmail API HttpError: Status {e.resp.status}, {e.error_details if hasattr(e, 'error_details') else str(e)}")
                        logger.warning("Falling back to mock data due to API error")
                    except Exception as e:
                        logger.error(f"Gmail API error: {type(e).__name__}: {e}")
                        logger.warning("Falling back to mock data due to error")
                else:
                    logger.warning("Gmail service not available, falling back to mock data")
            else:
                logger.debug("Gmail not configured, using mock data")
        except Exception as e:
            logger.error(f"Unexpected error in list_recent_messages: {type(e).__name__}: {e}")
            logger.warning("Falling back to mock data due to unexpected error")

        # Fallback to mock data if not configured or API fails
        logger.info("Using mock email data")
        return self._get_mock_messages(limit=limit)

    def send_reply(self, *, to: str, subject: str, body: str, thread_id: str | None = None) -> bool:
        """Send a reply email via Gmail API."""
        # In mock mode, just log and return success
        if self.settings.gmail_use_mock:
            logger.info(f"[MOCK] Would send reply to {to}: {subject[:50]}...")
            return True
        
        if not self.is_configured():
            logger.error("Cannot send reply: Gmail not configured")
            return False
        
        try:
            service = self._get_service()
            if not service:
                logger.error("Cannot send reply: Gmail service not available")
                return False
            
            # Create email message
            from email.mime.text import MIMEText
            
            message = MIMEText(body)
            message["To"] = to
            message["From"] = self.settings.gmail_user_email or "me"
            message["Subject"] = subject
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
            
            # Prepare message body
            message_body = {"raw": raw_message}
            if thread_id:
                message_body["threadId"] = thread_id
            
            # Send message
            logger.info(f"Sending reply to {to}: {subject[:50]}...")
            result = service.users().messages().send(userId="me", body=message_body).execute()
            logger.info(f"Reply sent successfully. Message ID: {result.get('id')}")
            return True
        except HttpError as e:
            logger.error(f"Failed to send reply via Gmail API: Status {e.resp.status}, {e.error_details if hasattr(e, 'error_details') else str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to send reply: {type(e).__name__}: {e}")
            return False

    def _get_mock_messages(self, *, limit: int = 10) -> Iterable[EmailMessage]:
        """Generate mock email messages for testing with varied content."""
        now = datetime.now(tz=timezone.utc)
        
        # Varied mock email templates to test different classifications
        mock_templates = [
            # Sales leads (lead_flag=True)
            {
                "sender": "prospect@example.com",
                "subject": "Demo inquiry",
                "snippet": "Interested in automation services",
                "body": "Hello, we would like to learn more about your AI automation offerings. Can we schedule a demo?",
            },
            {
                "sender": "buyer@company.com",
                "subject": "Pricing information request",
                "snippet": "Looking for pricing details",
                "body": "Hi, I'm interested in your product. Could you send me pricing information?",
            },
            # Support requests (lead_flag=False, category=SUPPORT_REQUEST)
            {
                "sender": "customer@example.com",
                "subject": "Issue with my account",
                "snippet": "Having trouble logging in",
                "body": "I'm having trouble logging into my account. Can you help me reset my password?",
            },
            {
                "sender": "user@example.com",
                "subject": "Bug report",
                "snippet": "Found a bug in the system",
                "body": "I found a bug when trying to export data. The export button doesn't work.",
            },
            # Internal emails (lead_flag=False, category=INTERNAL)
            {
                "sender": "colleague@company.com",
                "subject": "Team meeting tomorrow",
                "snippet": "Reminder about the meeting",
                "body": "Just a reminder that we have a team meeting tomorrow at 2 PM.",
            },
            {
                "sender": "manager@company.com",
                "subject": "Weekly report",
                "snippet": "Please review the report",
                "body": "Please review the weekly report and provide feedback by Friday.",
            },
            # Other/Spam (lead_flag=False, category=OTHER)
            {
                "sender": "newsletter@example.com",
                "subject": "Weekly newsletter",
                "snippet": "Your weekly digest",
                "body": "Here's your weekly newsletter with the latest updates.",
            },
            {
                "sender": "noreply@example.com",
                "subject": "Your order has shipped",
                "snippet": "Order confirmation",
                "body": "Your order #12345 has been shipped and will arrive in 3-5 business days.",
            },
            # More sales leads
            {
                "sender": "decision-maker@bigcorp.com",
                "subject": "Enterprise inquiry",
                "snippet": "Interested in enterprise solution",
                "body": "We're evaluating solutions for our enterprise. Can we discuss your enterprise features?",
            },
            {
                "sender": "startup@newco.io",
                "subject": "Partnership opportunity",
                "snippet": "Interested in partnership",
                "body": "We're a startup looking for partners. Would you be interested in a partnership?",
            },
        ]
        
        for idx in range(limit):
            template = mock_templates[idx % len(mock_templates)]
            yield EmailMessage(
                provider_id=f"mock-{idx}",
                thread_id=f"thread-{idx}",
                sender=template["sender"],
                recipients=[self.settings.gmail_user_email or "triage@example.com"],
                cc=[],
                subject=f"{template['subject']} #{idx}",
                snippet=template["snippet"],
                body=template["body"],
                received_at=now,
            )
