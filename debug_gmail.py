#!/usr/bin/env python3
"""Debug script to test Gmail connection."""

import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from app.core.config import get_settings
from app.providers.email.gmail import GmailProvider

def main():
    """Test Gmail connection and display debug information."""
    print("=" * 60)
    print("Gmail Connection Debug Tool")
    print("=" * 60)
    print()
    
    settings = get_settings()
    provider = GmailProvider(settings)
    
    # Check configuration
    print("1. Checking Configuration:")
    print(f"   Gmail Client ID: {'✓ Set' if settings.gmail_client_id else '✗ Not set'}")
    print(f"   Gmail Client Secret: {'✓ Set' if settings.gmail_client_secret else '✗ Not set'}")
    print(f"   Gmail Refresh Token: {'✓ Set' if settings.gmail_refresh_token else '✗ Not set'}")
    print(f"   Gmail User Email: {settings.gmail_user_email or '✗ Not set'}")
    print(f"   Is Configured: {provider.is_configured()}")
    print()
    
    if not provider.is_configured():
        print("❌ Gmail is not configured. Please check your .env file.")
        return 1
    
    # Test credentials
    print("2. Testing Credentials:")
    try:
        creds = provider._get_credentials()
        if creds:
            print("   ✓ Credentials created successfully")
            print(f"   Valid: {creds.valid}")
            print(f"   Expired: {creds.expired}")
            if creds.token:
                print(f"   Token (first 20 chars): {creds.token[:20]}...")
        else:
            print("   ✗ Failed to create credentials")
            return 1
    except Exception as e:
        print(f"   ✗ Error creating credentials: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    print()
    
    # Test service
    print("3. Testing Gmail API Service:")
    try:
        service = provider._get_service()
        if service:
            print("   ✓ Gmail service created successfully")
        else:
            print("   ✗ Failed to create Gmail service")
            return 1
    except Exception as e:
        print(f"   ✗ Error creating service: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    print()
    
    # Test API call
    print("4. Testing Gmail API Call:")
    try:
        results = (
            service.users()
            .messages()
            .list(userId="me", maxResults=5, q="is:inbox")
            .execute()
        )
        messages = results.get("messages", [])
        print(f"   ✓ API call successful")
        print(f"   Found {len(messages)} message(s) in inbox")
        
        if messages:
            print("\n   Sample messages:")
            for i, msg_ref in enumerate(messages[:3], 1):
                msg_id = msg_ref["id"]
                try:
                    msg = service.users().messages().get(userId="me", id=msg_id, format="metadata").execute()
                    headers = {h["name"].lower(): h["value"] for h in msg.get("payload", {}).get("headers", [])}
                    subject = headers.get("subject", "No subject")
                    sender = headers.get("from", "Unknown")
                    print(f"   {i}. {subject[:50]}... (from: {sender[:30]}...)")
                except Exception as e:
                    print(f"   {i}. Error fetching message {msg_id}: {e}")
        else:
            print("   (No messages found in inbox)")
    except HttpError as e:
        print(f"   ✗ Gmail API HttpError:")
        print(f"      Status: {e.resp.status}")
        print(f"      Error: {e.error_details if hasattr(e, 'error_details') else str(e)}")
        if e.resp.status == 401:
            print("      → This usually means the refresh token is invalid or expired")
        elif e.resp.status == 403:
            print("      → This usually means the app doesn't have permission")
        return 1
    except Exception as e:
        print(f"   ✗ Error calling Gmail API: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    print()
    
    # Test message fetching
    print("5. Testing Message Fetching (via provider):")
    try:
        messages = list(provider.list_recent_messages(limit=3))
        print(f"   ✓ Successfully fetched {len(messages)} message(s)")
        if messages:
            print("\n   Fetched messages:")
            for i, msg in enumerate(messages, 1):
                print(f"   {i}. Subject: {msg.subject[:50]}...")
                print(f"      From: {msg.sender[:50]}...")
                print(f"      Provider ID: {msg.provider_id}")
    except Exception as e:
        print(f"   ✗ Error fetching messages: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print()
    print("=" * 60)
    print("✓ All tests passed! Gmail connection is working.")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())

