#!/usr/bin/env python3
"""Get Gmail refresh token using provided OAuth credentials."""

import json
import os
import sys
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("Error: Missing required packages. Run: poetry install")
    sys.exit(1)

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_credentials_from_env_or_input():
    """Get OAuth credentials from environment or prompt user."""
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")

    if not client_id:
        print("Enter your Gmail OAuth Client ID:")
        print("(Get it from Google Cloud Console → Credentials → OAuth 2.0 Client ID)")
        client_id = input("Client ID: ").strip()
        if not client_id:
            print("Error: Client ID is required")
            sys.exit(1)

    if not client_secret:
        print("\nEnter your Gmail OAuth Client Secret:")
        client_secret = input("Client Secret: ").strip()
        if not client_secret:
            print("Error: Client Secret is required")
            sys.exit(1)

    return client_id, client_secret

def main():
    """Main function to get refresh token."""
    # Get credentials
    client_id, client_secret = get_credentials_from_env_or_input()

    # Create credentials dict in the format Google expects
    # Try both "installed" (desktop) and "web" (server-side) formats
    credentials_dict_installed = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost", "urn:ietf:wg:oauth:2.0:oob"]
        }
    }

    # Also try web application format (since you're using server-side flow)
    credentials_dict_web = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": ["http://localhost", "https://developers.google.com/oauthplayground"]
        }
    }

    # Use web format since you mentioned "Server-side" in the config
    credentials_dict = credentials_dict_web

    # Save to temporary file
    temp_credentials_file = "temp_gmail_credentials.json"
    with open(temp_credentials_file, "w") as f:
        json.dump(credentials_dict, f, indent=2)

    print("=" * 60)
    print("Gmail OAuth2 Refresh Token Generator")
    print("=" * 60)
    print()
    print("Starting OAuth2 flow...")
    print("A browser window will open for authentication.")
    print("Please authorize the application to access Gmail.")
    print()

    try:
    flow = InstalledAppFlow.from_client_secrets_file(
        temp_credentials_file, SCOPES
    )
    creds = flow.run_local_server(port=0, open_browser=True)
    
    # Clean up temp file
    Path(temp_credentials_file).unlink()
    
    if creds and creds.refresh_token:
        print()
        print("=" * 60)
        print("✓ Successfully obtained refresh token!")
        print("=" * 60)
        print()
        print("Add these to your .env file:")
        print()
        print(f"GMAIL_CLIENT_ID={client_id}")
        print(f"GMAIL_CLIENT_SECRET={client_secret}")
        print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
        print()
        print("=" * 60)
        print("⚠️  IMPORTANT: Add these to your .env file (not gmail_credentials.env)")
        print("   Never commit .env file to version control!")
        print()
        
        sys.exit(0)
    else:
        print("Error: No refresh token obtained")
        print("Make sure you granted offline access during authorization")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\nCancelled by user")
        Path(temp_credentials_file).unlink(missing_ok=True)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        Path(temp_credentials_file).unlink(missing_ok=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

