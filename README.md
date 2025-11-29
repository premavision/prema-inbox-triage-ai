# Inbox Triage AI

Production-style FastAPI prototype that syncs emails (Gmail), classifies them via LLM, and surfaces
suggested replies through a REST API and lightweight UI. Built for the Prema Vision portfolio.

## Features
- Gmail provider abstraction with mock data path (ready for real API integration)
- LLM abstraction with OpenAI implementation for classification + reply generation
- SQLModel persistence storing emails, metadata, and reply drafts
- FastAPI endpoints for syncing, listing, retrieving, retriaging, and sending emails
- Minimal Jinja2 UI for demoing the workflow with reply editing and sending
- Automatic classification and reply generation on sync
- Basic unit tests covering ingestion + classification services

## Tech stack
- Python 3.11, FastAPI, SQLModel/SQLite, Jinja2
- OpenAI Async client (pluggable via provider interface)
- Poetry for dependency + tooling management

## Architecture overview
```
app/
  core/            -> settings, logging
  db/              -> engine + metadata
  models/          -> SQLModel entities
  providers/       -> Email + LLM provider abstractions
  repositories/    -> data access layer
  services/        -> ingestion, classification, reply logic
  api/routes/      -> FastAPI routers
  ui/              -> templates + static assets
```
Providers and LLM clients expose small protocols (`EmailProvider`, `LLMClient`). Services depend on these
protocols + repositories, keeping domain logic framework-agnostic and easy to test.

## Getting started
1. Install Poetry and run `poetry install`.
2. (Optional) Copy `.env.example` to `.env` and configure:
   - For **mock mode** (default): No configuration needed - works out of the box!
   - For **real Gmail**: Set `GMAIL_USE_MOCK=false` and add Gmail OAuth credentials (see `GMAIL_OAUTH_SETUP.md`)
   - For **OpenAI features**: Add `OPENAI_API_KEY`
3. Launch the API + UI:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
4. Visit `http://127.0.0.1:8000/` for the dashboard.

**Note**: By default, the app uses mock email data. To use real Gmail, set `GMAIL_USE_MOCK=false` in `.env` and configure OAuth credentials. See `MOCK_VS_REAL.md` for details.

**Sending Replies**: To send replies via Gmail API, you need a refresh token with `gmail.send` scope. The app includes this scope, but if your current token only has `gmail.readonly`, you'll need to obtain a new refresh token. In mock mode, sending replies is simulated (logged but not actually sent).

## API reference
- `GET /health`
- `GET /config/providers`
- `POST /emails/sync` - Sync emails, automatically classify and generate replies
- `GET /emails?is_lead=true&priority=HIGH` - List emails with optional filters
- `GET /emails/{id}` - Get email details
- `POST /emails/{id}/retriage` - Re-classify email and generate reply
- `POST /emails/{id}/send` - Send a reply email (requires `gmail.send` scope)

## Testing
```
poetry run pytest
```

## Linting
```
poetry run ruff check .
poetry run black .
```

## Roadmap
- Real Gmail OAuth flow + incremental sync
- Background workers for classification/reply generation
- Additional providers (Outlook, HubSpot)
- Richer UI with filters and inline editing
