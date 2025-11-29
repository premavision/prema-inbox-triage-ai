# Gmail OAuth2 Setup Guide

## Step 1: Create OAuth 2.0 Credentials in Google Cloud Console

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Select your project (or create a new one)

2. **Enable Gmail API**
   - Go to "APIs & Services" → "Library"
   - Search for "Gmail API"
   - Click "Enable"

3. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen first:
     - User Type: External (or Internal if using Google Workspace)
     - App name: "Inbox Triage AI" (or any name)
     - User support email: your email
     - Developer contact: your email
     - Scopes: Add `https://www.googleapis.com/auth/gmail.readonly`
     - Test users: Add your Gmail address
   - Application type: **"Desktop app"** (important!)
   - Name: "Inbox Triage AI Desktop"
   - Click "Create"

4. **Download Credentials**
   - You'll see Client ID and Client Secret
   - **IMPORTANT**: Copy both values immediately
   - Format will be:
     ```
     Client ID: 123456789-abcdefghijklmnop.apps.googleusercontent.com
     Client Secret: GOCSPX-xxxxxxxxxxxxx
     ```

## Step 2: Get Refresh Token

### Option A: Using the provided script (Recommended)

```bash
poetry run python get_refresh_token.py
```

This will:
- Open a browser window
- Ask you to sign in with your Gmail account
- Request permission to access Gmail
- Generate a refresh token
- Save credentials to `gmail_credentials.env`

### Option B: Using OAuth Playground

1. Go to: https://developers.google.com/oauthplayground/
2. Click the gear icon (⚙️) in top right
3. Check "Use your own OAuth credentials"
4. Enter your Client ID and Client Secret
5. In the left panel, find "Gmail API v1"
6. Select scope: `https://www.googleapis.com/auth/gmail.readonly`
7. Click "Authorize APIs"
8. Sign in and grant permissions
9. Click "Exchange authorization code for tokens"
10. Copy the **Refresh token** (starts with `1//...`)

### Option C: Manual OAuth Flow

1. Build authorization URL:
   ```
   https://accounts.google.com/o/oauth2/v2/auth?
   client_id=YOUR_CLIENT_ID&
   redirect_uri=http://localhost:8080&
   response_type=code&
   scope=https://www.googleapis.com/auth/gmail.readonly&
   access_type=offline&
   prompt=consent
   ```

2. Open URL in browser, authorize, copy the `code` from redirect URL

3. Exchange code for tokens:
   ```bash
   curl -X POST https://oauth2.googleapis.com/token \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET" \
     -d "code=AUTHORIZATION_CODE" \
     -d "grant_type=authorization_code" \
     -d "redirect_uri=http://localhost:8080"
   ```

4. Copy the `refresh_token` from response

## Step 3: Configure .env File

Add these lines to your `.env` file:

```env
# Gmail OAuth2 Credentials
GMAIL_CLIENT_ID=your-client-id-here
GMAIL_CLIENT_SECRET=your-client-secret-here
GMAIL_REFRESH_TOKEN=your-refresh-token-here
GMAIL_USER_EMAIL=your-email@gmail.com
```

**Important Notes:**
- Use the **exact** Client ID and Client Secret from Google Cloud Console
- The refresh token must be obtained with the **same** Client ID/Secret
- Refresh token should start with `1//` or `1/`
- Make sure `access_type=offline` was used when getting the token
- Make sure `prompt=consent` was used (to force new token generation)

## Step 4: Test the Connection

```bash
# Clear settings cache and test
poetry run python debug_gmail.py
```

Expected output:
```
✓ Gmail Client ID: Set
✓ Gmail Client Secret: Set
✓ Gmail Refresh Token: Set
✓ Credentials created successfully
✓ Gmail service created successfully
✓ API call successful
```

## Common Issues and Solutions

### Issue: "invalid_grant: Bad Request"

**Causes:**
- Refresh token doesn't match Client ID/Secret
- Refresh token was obtained for different OAuth client
- Refresh token expired or was revoked
- Wrong application type (Web vs Desktop)

**Solutions:**
1. Make sure Client ID and Secret in `.env` match the ones used to get refresh token
2. If using OAuth Playground, make sure you entered your own credentials
3. Get a new refresh token using the script: `poetry run python get_refresh_token.py`
4. Make sure you're using "Desktop app" type, not "Web application"

### Issue: "Access blocked: This app's request is invalid"

**Solution:**
- Add your email as a test user in OAuth consent screen
- Make sure the app is in "Testing" mode (not "In production")

### Issue: No refresh token returned

**Solution:**
- Make sure `access_type=offline` is in the authorization URL
- Use `prompt=consent` to force consent screen
- If you've already authorized, revoke access and re-authorize

## Verification Checklist

- [ ] Gmail API is enabled in Google Cloud Console
- [ ] OAuth consent screen is configured
- [ ] OAuth client created as "Desktop app" type
- [ ] Client ID and Secret copied correctly
- [ ] Refresh token obtained with same Client ID/Secret
- [ ] `.env` file has all 4 Gmail variables set
- [ ] `debug_gmail.py` shows all checks passing
- [ ] Can successfully sync emails via API

## Quick Test Command

```bash
# Test connection
poetry run python debug_gmail.py

# Test sync
curl -X POST http://127.0.0.1:8000/emails/sync
```

