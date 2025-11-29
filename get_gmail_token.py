#!/usr/bin/env python3
"""Script to obtain Gmail OAuth2 refresh token."""

import os
import sys
from pathlib import Path

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("Error: Missing required packages. Run: poetry install")
    sys.exit(1)

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Token file
TOKEN_FILE = "gmail_token.json"
CREDENTIALS_FILE = "gmail_credentials.json"


def get_refresh_token():
    """Obtain a refresh token using OAuth2 flow."""
    creds = None

    # Check if we have a token file
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Token expired, refreshing...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Failed to refresh: {e}")
                print("Need to re-authenticate...")
                creds = None

        if not creds:
            if not os.path.exists(CREDENTIALS_FILE):
                print("=" * 60)
                print("Gmail OAuth2 Setup")
                print("=" * 60)
                print()
                print("You need to create a Gmail OAuth2 credentials file.")
                print()
                print("Steps:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project or select existing one")
                print("3. Enable Gmail API")
                print("4. Go to 'Credentials' → 'Create Credentials' → 'OAuth client ID'")
                print("5. Choose 'Desktop app' as application type")
                print("6. Download the credentials JSON file")
                print(f"7. Save it as '{CREDENTIALS_FILE}' in this directory")
                print()
                print("The credentials file should look like:")
                print('  {"installed": {"client_id": "...", "client_secret": "...", ...}}')
                print()
                sys.exit(1)

            print("Starting OAuth2 flow...")
            print("A browser window will open for authentication.")
            print()
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    # Extract refresh token
    if creds and creds.refresh_token:
        print("=" * 60)
        print("✓ Successfully obtained refresh token!")
        print("=" * 60)
        print()
        print("Add this to your .env file:")
        print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
        print()
        print("Also extract from your credentials file:")
        print(f"GMAIL_CLIENT_ID=<from credentials.json>")
        print(f"GMAIL_CLIENT_SECRET=<from credentials.json>")
        print()
        return creds.refresh_token
    else:
        print("Error: No refresh token obtained")
        return None


if __name__ == "__main__":
    try:
        refresh_token = get_refresh_token()
        if refresh_token:
            print("Refresh token obtained successfully!")
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

