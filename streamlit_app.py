import os
import streamlit as st
from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

def get_env(name: str):
    """
    Get environment variable from Streamlit secrets (Cloud) or os.getenv (Local).
    Priority: Streamlit secrets > os.getenv
    """
    if name in st.secrets:
        return st.secrets[name]
    return os.getenv(name)

# --- Configuration Setup ---
# Initialize session state for config if not present
if 'config' not in st.session_state:
    st.session_state.config = {
        'OPENAI_API_KEY': get_env("OPENAI_API_KEY"),
        'DATABASE_URL': get_env("DATABASE_URL"),
        'GMAIL_CLIENT_ID': get_env("GMAIL_CLIENT_ID"),
        'GMAIL_CLIENT_SECRET': get_env("GMAIL_CLIENT_SECRET"),
        'GMAIL_REFRESH_TOKEN': get_env("GMAIL_REFRESH_TOKEN"),
        'GMAIL_USER_EMAIL': get_env("GMAIL_USER_EMAIL"),
    }

st.title("Inbox Triage AI Configuration")

st.markdown("""
This app demonstrates the **Unified Secrets Management** approach.

- **Local Development**: Variables are loaded from `.env`.
- **Streamlit Cloud**: Variables are loaded from `st.secrets`.
""")

st.subheader("Current Environment Variables")

# Display loaded variables (masked for security)
for key, value in st.session_state.config.items():
    display_value = f"{value[:4]}...{value[-4:]}" if value and len(value) > 8 else (value or "Not Set")
    if key == "DATABASE_URL": # Show full DB URL usually fine locally, but masking is safer
         display_value = value if value else "Not Set"
    
    st.text_input(key, value=display_value, disabled=True)

if not st.session_state.config.get("OPENAI_API_KEY"):
    st.warning("⚠️ OPENAI_API_KEY is missing!")
else:
    st.success("✅ OPENAI_API_KEY is set.")
