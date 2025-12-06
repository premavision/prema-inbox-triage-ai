# End-to-End Tests

This directory contains comprehensive end-to-end (e2e) tests using Playwright for the Prema Inbox Triage AI application.

## Overview

The e2e test suite covers all use cases and user workflows:

- **API Endpoint Tests** (`test_api_endpoints.py`): Tests all REST API endpoints
- **UI Dashboard Tests** (`test_ui_dashboard.py`): Tests user interface interactions
- **Integration Workflow Tests** (`test_integration_workflows.py`): Tests complete user journeys

## Test Coverage

### API Endpoints
- ✅ Health check endpoint
- ✅ Provider configuration endpoint
- ✅ Email synchronization
- ✅ Email listing with filters (is_lead, category, priority)
- ✅ Email detail retrieval
- ✅ Email retriage/re-classification
- ✅ Reply sending

### UI Interactions
- ✅ Dashboard rendering and empty states
- ✅ Email sync from UI
- ✅ Email card display and structure
- ✅ View/hide email details
- ✅ Retriage unclassified emails
- ✅ Edit and send replies
- ✅ Loading states and form submissions

### Complete Workflows
- ✅ Full triage workflow (sync → classify → view → send)
- ✅ Manual retriage workflow
- ✅ Multiple email processing
- ✅ Data persistence across page loads
- ✅ Error handling and edge cases
- ✅ New user first-time setup
- ✅ Power user bulk operations

## Prerequisites

1. **Install Dependencies**
   ```bash
   poetry install
   ```

2. **Install Playwright Browsers**
   ```bash
   poetry run playwright install
   ```

## Running Tests

### Run All E2E Tests
```bash
poetry run pytest tests/e2e/ -v
```

### Run Specific Test Files
```bash
# API tests only
poetry run pytest tests/e2e/test_api_endpoints.py -v

# UI tests only
poetry run pytest tests/e2e/test_ui_dashboard.py -v

# Integration tests only
poetry run pytest tests/e2e/test_integration_workflows.py -v
```

### Run Specific Test Classes
```bash
poetry run pytest tests/e2e/test_api_endpoints.py::TestHealthEndpoint -v
```

### Run Specific Tests
```bash
poetry run pytest tests/e2e/test_ui_dashboard.py::TestDashboardRendering::test_dashboard_loads_successfully -v
```

### Run Single Test in UI Mode
See [Viewing Tests in UI](#-viewing-tests-in-ui) section below for detailed instructions on running individual tests with visual debugging.

### Run with Different Browser
```bash
PLAYWRIGHT_BROWSER=firefox poetry run pytest tests/e2e/ -v
PLAYWRIGHT_BROWSER=webkit poetry run pytest tests/e2e/ -v
```

### Run in Headed Mode (See Browser)
```bash
# Edit conftest.py to set headless=False, or use environment variable
PLAYWRIGHT_HEADED=true poetry run pytest tests/e2e/ -v
```

## 📋 Viewing All Tests (Without Running)

### Option 1: Cursor IDE / VS Code Test Explorer

#### For Cursor IDE:
Cursor is a fork of VS Code, but the Test Explorer may have limitations. Try these steps:

1. **Install Python Extension**
   - Open Extensions (Cmd/Ctrl + Shift + X)
   - Search for "Python" by Microsoft
   - Install it

2. **Configure Test Discovery**
   - Open Command Palette (Cmd/Ctrl + Shift + P)
   - Run: `Python: Configure Tests`
   - Select: `pytest`
   - Select: `tests/e2e` (or root directory)
   - Select: `Python file` or `Test file`

3. **Access Test Explorer**
   - Try: Command Palette → `Testing: Focus on Test Explorer View`
   - Or: Look for beaker icon in the sidebar
   - If Test Explorer doesn't appear, see workarounds below

#### If Test Explorer Doesn't Work in Cursor:
**Workaround 1: Use Command Palette**
- `Python: Run All Tests` - Lists and runs all tests
- `Python: Run Test Method` - Run specific test (place cursor in test)
- `Python: Run Test Class` - Run all tests in a class

**Workaround 2: Install Test Explorer Extensions**
- Search for "Test Explorer UI" extension
- Search for "Python Test Explorer" extension
- These may provide better test browsing in Cursor

**Workaround 3: Use Integrated Terminal**
- Open terminal in Cursor (Ctrl + `)
- Use `pytest --collect-only` to list tests
- Use code navigation to browse test files

#### For VS Code (Standard):
1. **Install Python Extension** (if not already installed)
   - Go to Extensions (Cmd/Ctrl + Shift + X)
   - Search for "Python" by Microsoft
   - Install it

2. **Configure Test Discovery**
   - Open Command Palette (Cmd/Ctrl + Shift + P)
   - Run: `Python: Configure Tests`
   - Select: `pytest`
   - Select: `tests/e2e` (or root directory)
   - Select: `Python file` or `Test file`

3. **View Tests**
   - Open the Test Explorer sidebar (beaker icon)
   - All tests will be listed in a tree structure
   - You can expand/collapse test classes
   - Click play buttons to run individual tests
   - Tests show as "not run" until you execute them

### Option 2: List Tests in Terminal
See all available tests without running them:

```bash
# List all tests
poetry run pytest tests/e2e/ --collect-only

# List with more details
poetry run pytest tests/e2e/ --collect-only -v

# List specific test file
poetry run pytest tests/e2e/test_ui_dashboard.py --collect-only -v

# Export test list to file
poetry run pytest tests/e2e/ --collect-only > test-list.txt
```

### Option 3: Generate Test Tree
Create a visual tree of all tests:

```bash
# Install pytest-tree (optional)
poetry add --group dev pytest-tree

# Show test tree
poetry run pytest tests/e2e/ --tree
```

### Option 4: Use pytest-html Report (Empty Run)
Generate an HTML report showing test structure:

```bash
# Run with --collect-only and generate report
poetry run pytest tests/e2e/ --collect-only --html=test-structure.html --self-contained-html

# Open the report
open test-structure.html
```

### Option 5: Use the Provided Script
A helper script is included to list all tests:

```bash
# Quick list
poetry run python tests/e2e/list_tests.py

# Verbose list with details
poetry run python tests/e2e/list_tests.py --verbose
```

This script uses `pytest --collect-only` to discover and list all tests without running them.

> **Note for Cursor IDE users**: See `CURSOR_IDE.md` for specific instructions on viewing and running tests in Cursor IDE.

## 🖥️ Viewing Tests in UI

### 1. Headed Browser Mode (See Browser Window)
See the actual browser window while tests run - great for watching what's happening:

```bash
# Run with visible browser window
poetry run pytest tests/e2e/ --headed -v

# Or use environment variable (works with our conftest.py)
PLAYWRIGHT_HEADED=true poetry run pytest tests/e2e/ -v

# Combine with specific browser
poetry run pytest tests/e2e/ --headed --browser=firefox -v
```

### 2. Playwright Inspector (Interactive Debugging) ⭐ Recommended
The best way to debug tests interactively - opens Playwright Inspector:

```bash
# Run with Playwright Inspector (interactive step-through)
PWDEBUG=1 poetry run pytest tests/e2e/ -s

# Or for specific test
PWDEBUG=1 poetry run pytest tests/e2e/test_ui_dashboard.py::TestDashboardRendering::test_dashboard_loads_successfully -s
```

### Running a Single Test in UI Mode

Here are examples for running **one specific test** with UI visibility:

#### Example 1: Single Test with Inspector (Best for Debugging)
```bash
# Run one specific test with Playwright Inspector
PWDEBUG=1 poetry run pytest tests/e2e/test_ui_dashboard.py::TestDashboardRendering::test_dashboard_loads_successfully -s
```

#### Example 2: Single Test with Headed Browser
```bash
# Run one test and see the browser window
poetry run pytest tests/e2e/test_ui_dashboard.py::TestDashboardRendering::test_dashboard_loads_successfully --headed -v
```

#### Example 3: Single Test from API Tests
```bash
# Run a specific API test with inspector
PWDEBUG=1 poetry run pytest tests/e2e/test_api_endpoints.py::TestHealthEndpoint::test_health_check_returns_ok -s
```

#### Example 4: Single Test from Integration Tests
```bash
# Run a workflow test with headed browser
poetry run pytest tests/e2e/test_integration_workflows.py::TestCompleteEmailTriageWorkflow::test_complete_workflow_sync_classify_view_send --headed -v
```

#### Test Path Format
The format for specifying a test is:
```
path/to/test_file.py::TestClassName::test_method_name
```

**Examples:**
- `tests/e2e/test_ui_dashboard.py::TestDashboardRendering::test_dashboard_loads_successfully`
- `tests/e2e/test_api_endpoints.py::TestEmailSyncEndpoint::test_sync_emails_returns_json`
- `tests/e2e/test_integration_workflows.py::TestCompleteEmailTriageWorkflow::test_complete_workflow_sync_classify_view_send`

#### Quick Tips for Single Test Debugging
1. **Use Inspector for step-by-step debugging**: `PWDEBUG=1 pytest <test_path> -s`
2. **Use headed mode to watch the browser**: `pytest <test_path> --headed -v`
3. **Combine both for maximum visibility**: `PWDEBUG=1 pytest <test_path> --headed -s`
4. **Add `-v` for verbose output** to see more details
5. **Add `-s` to see print statements** in your test code

This opens Playwright Inspector where you can:
- ✅ Step through tests line by line
- ✅ See browser actions in real-time
- ✅ Inspect page elements
- ✅ View console logs and network requests
- ✅ Pause and resume execution
- ✅ See the browser window alongside the inspector

### 3. HTML Test Reports
Generate a beautiful HTML report after tests complete:

```bash
# Install pytest-html (if not already installed)
poetry add --group dev pytest-html

# Generate HTML report
poetry run pytest tests/e2e/ --html=test-report.html --self-contained-html

# Open the report
open test-report.html  # macOS
# or
xdg-open test-report.html  # Linux
# or
start test-report.html  # Windows
```

The HTML report shows:
- ✅ Test results (passed/failed/skipped)
- ✅ Execution time
- ✅ Error messages and stack traces
- ✅ Test coverage summary

### 4. Playwright Trace Viewer
View detailed traces of test execution:

```bash
# Run tests with trace
poetry run pytest tests/e2e/ --tracing=on

# View trace (opens in browser)
poetry run playwright show-trace trace.zip
```

### 5. Cursor IDE / VS Code Test Explorer
If using Cursor or VS Code, use the built-in test explorer:

1. Install "Python" extension (if not already installed)
2. Open Command Palette (Cmd/Ctrl + Shift + P)
3. Run "Python: Configure Tests"
4. Select "pytest" as test framework
5. Tests will appear in the Test Explorer sidebar
6. Click play buttons to run individual tests
7. See results inline with your code

### Quick Reference

| Method | Command | Best For |
|--------|---------|----------|
| **Headed Mode** | `pytest --headed` | Watching browser actions |
| **Inspector** | `PWDEBUG=1 pytest -s` | Debugging and step-through |
| **HTML Report** | `pytest --html=report.html` | Sharing results |
| **Trace Viewer** | `pytest --tracing=on` | Detailed execution analysis |
| **Cursor/VS Code** | Use Test Explorer or Command Palette | IDE integration |

## Test Configuration

### Test Server
- Tests automatically start a FastAPI server on `http://127.0.0.1:8000`
- Uses a separate test database (`test_inbox.db`) to avoid interfering with development
- Server is automatically stopped after tests complete
- Uses mock email provider by default (no real Gmail API needed)

### Test Database
- Test database is created in the project root as `test_inbox.db`
- Automatically cleaned up after test session completes
- Each test session starts with a fresh database

### Browser Configuration
- Default: Chromium in headless mode
- Can be changed via `PLAYWRIGHT_BROWSER` environment variable
- Viewport: 1280x720
- Locale: en-US

## Test Structure

### Fixtures
- `test_server_process`: Starts/stops the FastAPI server
- `base_url`: Returns the test server URL
- `playwright`: Playwright instance
- `browser`: Browser instance
- `context`: Browser context (fresh for each test)
- `page`: Browser page (fresh for each test)
- `api_request_context`: For API testing without browser

### Test Organization
Tests are organized by functionality:
- **API Tests**: Test endpoints directly via HTTP requests
- **UI Tests**: Test user interactions via browser automation
- **Integration Tests**: Test complete workflows combining API and UI

## Writing New Tests

### Example: API Test
```python
def test_my_endpoint(self, api_request_context: APIRequestContext):
    """Test description explaining what this verifies."""
    response = api_request_context.get("/my/endpoint")
    expect(response).to_be_ok()
    data = response.json()
    assert data["field"] == "expected_value"
```

### Example: UI Test
```python
def test_my_ui_feature(self, page: Page, base_url: str):
    """Test description explaining what this verifies."""
    page.goto(base_url)
    button = page.locator("button:has-text('My Button')")
    expect(button).to_be_visible()
    button.click()
    expect(page.locator(".result")).to_be_visible()
```

## Best Practices

1. **Descriptive Test Names**: Test names should clearly describe what they verify
2. **Docstrings**: Each test should have a docstring explaining its purpose
3. **Test Isolation**: Each test should be independent and not rely on others
4. **Wait for Operations**: Use `wait_for_load_state()` and timeouts appropriately
5. **Assertions**: Use Playwright's `expect()` for better error messages
6. **Error Handling**: Tests should handle cases where elements might not exist

## Troubleshooting

### Server Fails to Start
- Check if port 8000 is already in use
- Verify poetry and dependencies are installed
- Check server logs in test output

### Tests Timeout
- Increase timeout values if needed
- Check that server is actually running
- Verify network connectivity

### Browser Issues
- Run `poetry run playwright install` to ensure browsers are installed
- Try a different browser via `PLAYWRIGHT_BROWSER`
- Check Playwright version compatibility

### Database Issues
- Ensure test database file can be created/deleted
- Check file permissions in project directory
- Verify SQLite is working correctly

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Headless browser mode by default
- Automatic server startup/teardown
- Isolated test database
- No external dependencies required (uses mock provider)

## Notes

- Tests use the mock email provider by default (no Gmail API needed)
- **LLM classification may be slow**; tests include appropriate timeouts (60 seconds for sync/retriage operations)
- Some tests check for optional features (e.g., suggested replies) and skip if not available
- Tests are designed to be resilient to timing variations

## Handling Slow Operations

If tests timeout, it's likely because LLM classification is taking longer than expected. The tests use:
- `page.expect_navigation(timeout=60000)` for form submissions that trigger classification
- `page.wait_for_timeout(2000)` after sync operations to allow classification to complete
- Default page timeout of 30 seconds (can be increased if needed)

If you see timeout errors, try:
1. Increasing the timeout in the specific test
2. Adding `page.wait_for_timeout()` after slow operations
3. Using `wait_until="domcontentloaded"` instead of `"networkidle"` for faster checks

