# Inbox Triage AI

Production-style FastAPI prototype that syncs emails (Gmail), classifies them via LLM, and surfaces
suggested replies through a REST API and lightweight UI. Built for the Prema Vision portfolio.

## Features
- Gmail provider abstraction with mock data path (ready for real API integration)
- LLM abstraction with OpenAI implementation for classification + reply generation
- SQLModel persistence storing emails, metadata, and reply drafts
- FastAPI endpoints for syncing, listing, retrieving, and retriaging emails
- Minimal Jinja2 UI for demoing the workflow
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
2. Copy `.env.example` to `.env` and fill in credentials (mock Gmail + OpenAI key).
3. Initialize the database:
   ```bash
   poetry run python -c "from sqlmodel import SQLModel; from app.db.session import engine; import app.models.email  # noqa; SQLModel.metadata.create_all(engine)"
   ```
   or simply start the app once (SQLModel will create tables automatically).
4. Launch the API + UI:
   ```bash
   poetry run uvicorn app.main:app --reload
   ```
5. Visit `http://127.0.0.1:8000/` for the dashboard.

## API reference
- `GET /health`
- `GET /config/providers`
- `POST /emails/sync`
- `GET /emails?is_lead=true&priority=HIGH`
- `GET /emails/{id}`
- `POST /emails/{id}/retriage`

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
