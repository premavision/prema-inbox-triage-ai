# User Roles, Entry Points, and Flows

## Main User Roles

*   **Operator** (Sales/Support Ops): The primary user who monitors the dashboard, reviews AI classifications, edits drafts, and approves outgoing replies.
*   **System Admin**: Responsible for initial configuration (Gmail OAuth setup, environment variables), though this is largely a setup-time role.

## Entry Points

### Web Interface (Dashboard)
*   **Main Dashboard (`/`)**: The central control center containing the inbox view, control buttons ("Sync", "Reset"), and email detail cards.

### API Endpoints (Backend)
*   **Sync & Process**: `POST /emails/sync` (Ingests and runs AI pipeline)
*   **Email Operations**:
    *   `POST /emails/{id}/send` (Dispatch reply)
    *   `POST /emails/{id}/retriage` (Re-classify)
    *   `POST /emails/{id}/generate-reply` (Draft creation)
*   **Management**: `POST /emails/reset` (Clear database)

## Key User Flows

### 1. Inbox Synchronization & Auto-Triage
**User Intent**: Fetch recent emails and have the AI automatically organize and draft responses for them.
*   **Step 1**: User clicks the **"Sync Latest Emails"** button on the dashboard.
*   **System Response**:
    1.  Fetches new emails from Gmail (or Mock provider).
    2.  Classifies emails by intent (Sales Lead, Support, Internal, etc.).
    3.  Assigns priority scores and flags "Leads".
    4.  Auto-generates draft replies for relevant categories.
    5.  Refreshes the inbox list with new cards displaying badges (e.g., "⭐ Lead", "Sales Lead").

### 2. Review & Send Reply (The "Human-in-the-Loop")
**User Intent**: Verify an AI-written draft, make necessary edits, and send the response.
*   **Step 1**: User identifies an email card with a `Reply Drafted` status and clicks **"View Details"**.
*   **System Response**: Expands the card to show the full email body and the AI-suggested reply in an editable text area.
*   **Step 2**: User edits the draft text to add personal context or correct details.
*   **Step 3**: User clicks **"Send Reply"**.
*   **System Response**:
    1.  Dispatches the email via Gmail.
    2.  Updates the email status to `Reply Sent`.
    3.  Locks the text area to prevent further edits.

### 3. Manual Assistance (On-Demand Generation)
**User Intent**: Request an AI draft for an email that was skipped or requires a specific response.
*   **Step 1**: User expands an email that has no draft and clicks **"Generate Reply"**.
*   **System Response**: Calls the LLM to generate a draft based on the email context and populates the reply box.
*   **Step 2**: User reviews/edits and clicks **"Send Reply"**.
*   **System Response**: Sends the email and updates status to `Reply Sent`.

### 4. Retriage / Error Recovery
**User Intent**: Force the system to re-evaluate an email that wasn't processed correctly (e.g., missing category).
*   **Step 1**: User sees an email in a "Pending" or uncategorized state and clicks **"Classify & Reply"**.
*   **System Response**:
    1.  Re-runs the classification service.
    2.  Updates the category and priority badges.
    3.  Attempts to generate a draft reply if applicable.

### 5. System Reset (Demo Mode)
**User Intent**: Clear all data to demonstrate the workflow from a clean slate.
*   **Step 1**: User clicks **"Reset Data"**.
*   **Step 2**: User confirms the browser alert dialog.
*   **System Response**:
    1.  Deletes all email records from the database.
    2.  Resets the mock email provider state.
    3.  Clears the dashboard list (shows "No emails yet").
