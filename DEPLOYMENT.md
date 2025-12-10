# Deployment Guide

This project is designed to be deployed as a separated Backend (FastAPI) and Frontend (React/Vite) application.

## Architecture

- **Backend:** FastAPI (Python) -> Deployed on **Render**.
- **Frontend:** React + Vite (TypeScript) -> Deployed on **Vercel**.
- **Database:** SQLite (Ephemeral) -> Resets on every deployment/restart (ideal for Demo mode).

---

## Part 1: Backend Deployment (Render.com)

1.  **Create a New Web Service**
    *   Go to [Render Dashboard](https://dashboard.render.com/).
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub repository.

2.  **Configure Service**
    *   **Name:** `prema-api` (or your choice)
    *   **Region:** Frankfurt (or closest to you)
    *   **Runtime:** Python 3
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`

3.  **Environment Variables**
    Add the following variables in the "Environment" tab:

    | Key | Value | Description |
    |-----|-------|-------------|
    | `PYTHON_VERSION` | `3.11.9` | Ensure Python version matches |
    | `APP_ENV` | `production` | Sets app to prod mode |
    | `OPENAI_API_KEY` | `sk-...` | Your actual OpenAI API Key |
    | `ALLOWED_ORIGINS` | `["*"]` | Temporarily allow all, or wait until Part 2 to set specific URL |

4.  **Deploy**
    *   Click **Create Web Service**.
    *   Wait for the build to finish.
    *   **Copy the Service URL** (e.g., `https://prema-api.onrender.com`). You will need this for the frontend.

    > **Note on Database:** Since we are using SQLite on Render's ephemeral filesystem, the database will be wiped and re-seeded with demo data every time you redeploy or restart the service.

---

## Part 2: Frontend Deployment (Vercel)

1.  **Create a New Project**
    *   Go to [Vercel Dashboard](https://vercel.com/dashboard).
    *   Click **Add New...** -> **Project**.
    *   Import the same GitHub repository.

2.  **Project Settings (CRITICAL)**
    *   **Framework Preset:** Vite
    *   **Root Directory:** Click `Edit` and select `frontend`.
        *   *If you skip this, the build will fail because package.json is not in the root.*

3.  **Environment Variables**
    Add the following variable:

    | Key | Value | Description |
    |-----|-------|-------------|
    | `VITE_API_URL` | `https://your-app.onrender.com` | The URL from Part 1 (**No trailing slash**) |

4.  **Deploy**
    *   Click **Deploy**.
    *   Vercel will build the React app and give you a domain (e.g., `https://prema-inbox.vercel.app`).

---

## Part 3: Final Connection (CORS)

To ensure the Frontend can talk to the Backend securely:

1.  Copy your new Vercel domain (e.g., `https://prema-inbox.vercel.app`).
2.  Go back to **Render Dashboard** -> **Environment**.
3.  Update (or Create) the `ALLOWED_ORIGINS` variable:

    ```json
    ["https://prema-inbox.vercel.app", "http://localhost:5173"]
    ```
    *(Note: It must be a valid JSON array string).*

4.  **Save Changes**. Render will automatically restart the backend.

---

## Verification

1.  Open your Vercel URL.
2.  You should see the Dashboard.
3.  The app should automatically load 4 demo emails (seeded by the backend).
4.  If you see "Network Error", check the Console (F12) to ensure `VITE_API_URL` is correct and CORS is configured.
