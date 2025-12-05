"""E2E test configuration and fixtures."""

import os
import subprocess
import time
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

# Get the project root directory
ROOT_DIR = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def test_database_url() -> str:
    """Return a test database URL that won't interfere with development database."""
    return "sqlite:///./test_inbox_data"


@pytest.fixture(scope="session")
def test_server_process(test_database_url: str) -> Generator[subprocess.Popen, None, None]:
    """
    Start the FastAPI server for testing.
    
    This fixture starts a uvicorn server in the background with a test database.
    The server runs on http://127.0.0.1:8000 and is automatically stopped after tests.
    """
    # Set environment variables for test server
    env = os.environ.copy()
    env["DATABASE_URL"] = test_database_url
    env["GMAIL_USE_MOCK"] = "true"  # Use mock provider for tests
    env["OPENAI_API_KEY"] = "mock"  # Use mock LLM for tests
    env["APP_ENV"] = "test"
    
    # Start the server
    process = subprocess.Popen(
        ["poetry", "run", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001"],
        cwd=ROOT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    # Wait for server to be ready
    max_attempts = 30
    for _ in range(max_attempts):
        try:
            import httpx
            response = httpx.get("http://127.0.0.1:8001/health", timeout=1.0)
            if response.status_code == 200:
                break
        except Exception:
            time.sleep(0.5)
    else:
        process.terminate()
        raise RuntimeError("Test server failed to start within 15 seconds")
    
    yield process
    
    # Cleanup: stop the server
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        print("Server didn't shutdown gracefully, forcing kill...")
        process.kill()
        process.wait()
    
    # Clean up test database
    test_db_path = ROOT_DIR / "test_inbox_data"
    if test_db_path.exists():
        test_db_path.unlink()


@pytest.fixture(scope="session", autouse=True)
def ensure_server_running(test_server_process: subprocess.Popen) -> None:
    """
    Ensure the test server is running before any tests execute.
    
    This fixture is autouse=True, so it runs automatically for all tests.
    It depends on test_server_process, ensuring the server starts first.
    """
    pass  # The dependency on test_server_process ensures it runs


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the test server."""
    return "http://127.0.0.1:8001"


@pytest.fixture(scope="session")
def playwright() -> Generator[Playwright, None, None]:
    """Initialize Playwright for the test session."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright: Playwright) -> Generator[Browser, None, None]:
    """
    Launch a browser instance for testing.
    
    Uses Chromium in headless mode by default. Can be overridden with:
    - PLAYWRIGHT_BROWSER environment variable (chromium, firefox, webkit)
    - PLAYWRIGHT_HEADED environment variable (true/false) to show browser window
    """
    browser_type = os.getenv("PLAYWRIGHT_BROWSER", "chromium")
    browser_name = getattr(playwright, browser_type)
    
    # Check if headed mode is requested
    headed = os.getenv("PLAYWRIGHT_HEADED", "false").lower() == "true"
    
    browser = browser_name.launch(headless=not headed)
    yield browser
    browser.close()


@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Create a new browser context for each test.
    
    This ensures test isolation - each test gets a fresh browser context
    with its own cookies, localStorage, and session storage.
    """
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        locale="en-US",
    )
    yield context
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    """
    Create a new page for each test.
    
    This is the main fixture for UI tests. Each test gets a fresh page
    that navigates to the base URL automatically.
    
    Note: Default timeout is set to 30 seconds, but slow operations
    (like LLM classification) may need longer timeouts. Use
    `page.expect_navigation(timeout=60000)` for form submissions.
    """
    page = context.new_page()
    # Set default timeout to 60 seconds (increased for LLM operations)
    page.set_default_timeout(60000)
    return page

