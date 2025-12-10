import logging
from datetime import datetime
from sqlmodel import Session
from app.db.session import engine
from app.models.email import Email
from app.core.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_emails():
    """Seed the database with demo emails if empty."""
    settings = get_settings()
    
    with Session(engine) as session:
        # Check if DB is initialized/connected properly
        try:
            existing = session.query(Email).first()
            if existing:
                logger.info("Database already contains data. Skipping seed.")
                return
        except Exception as e:
            logger.warning(f"Could not query database (tables might not exist yet): {e}")
            return

        logger.info("Seeding database with demo emails...")
        
        # Use simple strings matching the model definition in app/models/email.py
        # There are no Enum classes in the current model file.
        
        demo_emails = [
            Email(
                subject="Enterprise License Inquiry",
                sender="john.doe@bigcorp.com",
                recipients="sales@premavision.net",
                body="Hello, we are interested in purchasing 500 seats for your platform. Do you offer volume discounts?",
                snippet="interested in purchasing 500 seats",
                processing_status="processed", # Using 'processed' to show results immediately
                category="SALES_LEAD",
                lead_flag=True,
                priority="high",
                provider_id="mock-1",
                received_at=datetime.utcnow()
            ),
            Email(
                subject="Login issues",
                sender="sarah@startup.io",
                recipients="support@premavision.net",
                body="I cannot reset my password. The link sends me to a 404 page. Please help asap.",
                snippet="cannot reset my password",
                processing_status="processed",
                category="SUPPORT_REQUEST",
                lead_flag=False,
                priority="high",
                provider_id="mock-2",
                received_at=datetime.utcnow()
            ),
            Email(
                subject="Weekly Team Sync",
                sender="boss@premavision.net",
                recipients="team@premavision.net",
                body="Let's meet on Friday to discuss the Q3 roadmap. Please update your slides.",
                snippet="meet on Friday to discuss Q3",
                processing_status="processed",
                category="INTERNAL",
                lead_flag=False,
                priority="medium",
                provider_id="mock-3",
                received_at=datetime.utcnow()
            ),
            Email(
                subject="Invoice #10234",
                sender="billing@saas-tool.com",
                recipients="finance@premavision.net",
                body="Please find attached the invoice for July services.",
                snippet="attached the invoice for July",
                processing_status="processed",
                category="OTHER",
                lead_flag=False,
                priority="low",
                provider_id="mock-4",
                received_at=datetime.utcnow()
            )
        ]

        for email in demo_emails:
            session.add(email)
        
        session.commit()
        logger.info(f"Added {len(demo_emails)} demo emails.")

if __name__ == "__main__":
    seed_emails()
