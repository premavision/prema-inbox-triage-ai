# Gmail Mock vs Real Mode

## Overview

The application supports two modes for Gmail email fetching:
- **Mock Mode** (default): Uses simulated email data for testing
- **Real Mode**: Connects to actual Gmail API to fetch real emails

## Configuration

### Default Behavior

By default, the application uses **mock mode** (`GMAIL_USE_MOCK=true`). This means:
- No Gmail API credentials are required
- Mock email data is generated automatically
- Safe for development and testing
- No risk of hitting API rate limits

### Switching to Real Gmail

To use real Gmail API:

1. **Set in `.env` file:**
   ```env
   GMAIL_USE_MOCK=false
   GMAIL_CLIENT_ID=your-client-id
   GMAIL_CLIENT_SECRET=your-client-secret
   GMAIL_REFRESH_TOKEN=your-refresh-token
   GMAIL_USER_EMAIL=your-email@gmail.com
   ```

2. **Restart the server** to pick up new settings

3. **Verify the mode:**
   ```bash
   curl http://127.0.0.1:8000/config/providers
   ```
   Check the `details.mode` field - should show `"real"` or `"mock"`

## How It Works

### Mock Mode (`GMAIL_USE_MOCK=true`)
- Generates 10 mock emails with subjects like "Demo inquiry #0", "#1", etc.
- All emails have the same content structure
- No API calls are made
- Fast and reliable for testing

### Real Mode (`GMAIL_USE_MOCK=false`)
- Connects to Gmail API using OAuth2 credentials
- Fetches actual emails from your Gmail inbox
- Requires valid credentials (see `GMAIL_OAUTH_SETUP.md`)
- Falls back to mock if:
  - Credentials are invalid
  - API call fails
  - Service is unavailable

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GMAIL_USE_MOCK` | `true` | Enable mock mode (true) or real Gmail API (false) |
| `GMAIL_ENABLED` | `true` | Enable/disable Gmail provider entirely |
| `GMAIL_CLIENT_ID` | `None` | OAuth2 Client ID (required for real mode) |
| `GMAIL_CLIENT_SECRET` | `None` | OAuth2 Client Secret (required for real mode) |
| `GMAIL_REFRESH_TOKEN` | `None` | OAuth2 Refresh Token (required for real mode) |
| `GMAIL_USER_EMAIL` | `None` | Your Gmail address (optional, used in mock mode) |

## Examples

### Using Mock Mode (Default)
```bash
# No configuration needed - just start the server
poetry run uvicorn app.main:app --reload

# Or explicitly set in .env
GMAIL_USE_MOCK=true
```

### Using Real Gmail
```bash
# In .env file
GMAIL_USE_MOCK=false
GMAIL_CLIENT_ID=your-client-id
GMAIL_CLIENT_SECRET=your-client-secret
GMAIL_REFRESH_TOKEN=your-refresh-token
GMAIL_USER_EMAIL=your-email@gmail.com
```

## Checking Current Mode

### Via API
```bash
curl http://127.0.0.1:8000/config/providers | jq '.providers[0].details.mode'
```

### Via Code
```python
from app.core.config import get_settings
settings = get_settings()
print(f"Mock mode: {settings.gmail_use_mock}")
```

## Benefits of Mock Mode

1. **No API Setup Required**: Works out of the box
2. **Fast Development**: No network calls, instant responses
3. **Predictable Data**: Same emails every time for testing
4. **No Rate Limits**: Can test extensively without API restrictions
5. **Privacy**: No real email data exposed during development

## When to Use Real Mode

- Production deployment
- Testing with actual email data
- Demonstrating real Gmail integration
- Development of Gmail-specific features

