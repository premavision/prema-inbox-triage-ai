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

- **Modern React UI**
  - Dashboard for operators to view inbox, inspect messages, and manage replies
  - Built with React, Vite, and TypeScript

- **Persistence layer**
  - SQLModel + SQLite
  - Emails, metadata, replies, triage states

- **Testable modular architecture**
  - EmailProvider, LLMClient, Repositories, Services
  - Mock providers for unit testing

---

## 🌐 Live Demo

- **Web UI:** https://prema-inbox-triage-ai.vercel.app
- **API docs (Swagger):** https://prema-inbox-triage-ai.onrender.com/docs


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
  ui/              # legacy Jinja2 dashboard (server-rendered)
frontend/          # Modern React + Vite application
tests/             # unit tests + e2e tests (Playwright)
```

---

## ⚙️ Getting Started

### 1. Install Backend Dependencies

```bash
poetry install
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Configure Environment (optional)

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

This project follows a monolithic approach with both backend and frontend in the same repository. You will need two terminal sessions to run the full stack.

### 1. Start the Backend API

```bash
poetry run uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 2. Start the Frontend UI

Open a new terminal:

```bash
cd frontend
npm run dev
```

Open the UI:

```
http://localhost:5173/
```

The frontend development server is configured to proxy API requests to the backend at port 8000.

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

### Unit Tests
```bash
poetry run pytest
```

### End-to-End Tests
Comprehensive e2e tests using Playwright covering all API endpoints, UI interactions, and complete workflows.

**Setup:**
```bash
poetry install  # Installs playwright dependencies
poetry run playwright install  # Installs browser binaries
```

**Run e2e tests:**
```bash
# All e2e tests
poetry run pytest tests/e2e/ -v

# Specific test suites
poetry run pytest tests/e2e/test_api_endpoints.py -v
poetry run pytest tests/e2e/test_ui_dashboard.py -v
poetry run pytest tests/e2e/test_integration_workflows.py -v
```

See `tests/e2e/README.md` for detailed documentation.

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
