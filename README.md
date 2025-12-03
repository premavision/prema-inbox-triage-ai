# Prema Inbox Triage AI

Production-style FastAPI application that syncs Gmail inboxes, classifies messages using an LLM, and generates suggested replies.  
Part of the **Prema Vision AI Automations** portfolio.

---

## 🚀 Features

- **Gmail provider abstraction**  
  - Mock email provider (works out of the box)  
  - Real Gmail API support via OAuth (optional)

- **LLM-powered classification & reply generation**  
  - Provider interface with OpenAI implementation  
  - Draft replies stored and editable in the UI

- **Email ingestion & workflow automation**  
  - Automatic classification on sync  
  - Reply suggestion generation  
  - Re-triaging endpoint

- **Lightweight UI for operators**  
  - Jinja2 templates  
  - View inbox, inspect messages, edit replies, send replies

- **Persistence layer**  
  - SQLModel + SQLite  
  - Emails, metadata, replies, triage states

- **Testable modular architecture**  
  - EmailProvider, LLMClient, Repositories, Services  
  - Mock providers for unit testing

---

## 🧱 Project Structure

```
app/
  core/            # settings, logging
  db/              # database init + engine
  models/          # SQLModel ORM entities
  providers/       # Gmail + mock providers, LLM providers
  repositories/    # data access layer
  services/        # ingestion, classification, reply logic
  api/routes/      # FastAPI routers
  ui/              # minimal Jinja2 dashboard
tests/             # unit tests
```

---

## ⚙️ Getting Started

### 1. Install Dependencies

```bash
poetry install
```

### 2. Configure Environment (optional)

Copy env template:

```bash
cp .env.example .env
```

Modes:

| Mode | Description | Requirements |
|------|-------------|--------------|
| **Mock (default)** | Uses built-in example emails | No config needed |
| **Real Gmail** | Uses Gmail API to fetch/send emails | OAuth credentials + refresh token |
| **OpenAI** | Uses LLM for classification & replies | `OPENAI_API_KEY` |

See:  
- `GMAIL_OAUTH_SETUP.md`  
- `MOCK_VS_REAL.md`

---

## ▶️ Run the App

```bash
poetry run uvicorn app.main:app --reload
```

Open the UI:

```
http://127.0.0.1:8000/
```

---

## 📨 Sending Replies

- Mock mode → replies are logged (not sent)  
- Real Gmail → requires token with `gmail.send` scope  
- If your token only has `gmail.readonly`, generate a new one

---

## 🛠 API Endpoints

| Method | Endpoint | Description |
|-------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/emails/sync` | Sync inbox, auto-classify emails |
| GET | `/emails` | List emails (filters supported) |
| GET | `/emails/{id}` | Get email details |
| POST | `/emails/{id}/retriage` | Re-run LLM classification |
| POST | `/emails/{id}/send` | Send reply email |

---

## 🧪 Testing

```bash
poetry run pytest
```

---

## 🧹 Tooling

```bash
poetry run ruff check .
poetry run black .
```

---

## 🗺 Roadmap

- Real Gmail OAuth flow with token refresh
- Background tasks for async classification
- Additional providers (Outlook, HubSpot)
- Improved UI (filters, inline editing)
- Lead-scoring & tighter CRM workflows

---

## 🤝 Contributions

Issues and PRs are welcome.  
Part of the **Prema Vision AI Automation portfolio**.
