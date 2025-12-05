# Using E2E Tests in Cursor IDE

This guide provides specific instructions for viewing and running e2e tests in Cursor IDE.

## Quick Start

### View All Tests Without Running

**Method 1: Command Palette (Recommended)**
1. Open Command Palette: `Cmd/Ctrl + Shift + P`
2. Type: `Python: Configure Tests`
3. Select: `pytest`
4. Select: `tests/e2e` directory
5. Use these commands to view/run tests:
   - `Python: Run All Tests` - See all tests and run them
   - `Python: Run Test Method` - Run test at cursor
   - `Python: Run Test Class` - Run all tests in current class

**Method 2: Terminal**
```bash
# List all tests
poetry run pytest tests/e2e/ --collect-only -v

# Or use the helper script
poetry run python tests/e2e/list_tests.py --verbose
```

**Method 3: Code Navigation**
- Open test files in Cursor
- Use Outline view (Cmd/Ctrl + Shift + O) to see test structure
- Navigate between test files using file explorer

## Running Tests in Cursor

### Run Single Test
1. Place cursor inside a test method
2. Command Palette: `Python: Run Test Method`
3. Or right-click → `Run Test`

### Run All Tests in a Class
1. Place cursor in the test class
2. Command Palette: `Python: Run Test Class`

### Run All Tests
1. Command Palette: `Python: Run All Tests`

### Run from Terminal
```bash
# Single test
poetry run pytest tests/e2e/test_ui_dashboard.py::TestDashboardRendering::test_dashboard_loads_successfully -v

# All tests
poetry run pytest tests/e2e/ -v

# With UI (headed mode)
poetry run pytest tests/e2e/ --headed -v

# With inspector
PWDEBUG=1 poetry run pytest tests/e2e/ -s
```

## Debugging Tests in Cursor

### Using Python Debugger
1. Set breakpoint in test code
2. Command Palette: `Python: Debug Test Method`
3. Or right-click → `Debug Test`

### Using Playwright Inspector
```bash
PWDEBUG=1 poetry run pytest tests/e2e/test_ui_dashboard.py::TestEmailSyncUI::test_sync_button_triggers_sync -s
```

This opens Playwright Inspector where you can:
- Step through tests line by line
- See browser actions in real-time
- Inspect page elements
- View console logs

## Cursor-Specific Tips

### If Test Explorer Doesn't Appear
Cursor may not show the Test Explorer sidebar. Use these alternatives:

1. **Command Palette Commands**
   - `Python: Run All Tests` - Lists tests in output panel
   - `Python: Run Test Method` - Quick test execution

2. **Install Test Explorer Extensions**
   - Search for "Test Explorer UI" in Extensions
   - Search for "Python Test Explorer" 
   - These may provide better test browsing

3. **Use Integrated Terminal**
   - Open terminal: `Ctrl + `` (backtick)
   - Run `pytest --collect-only` to see all tests
   - Use terminal for all test operations

### Keyboard Shortcuts
- `Cmd/Ctrl + Shift + P` - Command Palette
- `Ctrl + `` - Toggle Terminal
- `Cmd/Ctrl + Shift + O` - Outline (test structure in file)

### File Navigation
- `Cmd/Ctrl + P` - Quick file open
- Type `test_` to find test files quickly
- Use file explorer to browse `tests/e2e/` directory

## Recommended Workflow

1. **Browse Tests**: Use file explorer or `pytest --collect-only`
2. **Run Single Test**: Place cursor in test → `Python: Run Test Method`
3. **Debug Test**: Set breakpoint → `Python: Debug Test Method`
4. **Watch Browser**: Use `--headed` flag in terminal
5. **Step Through**: Use `PWDEBUG=1` for Playwright Inspector

## Troubleshooting

### Tests Not Discovered
- Check Python extension is installed
- Verify `pytest` is in your Poetry environment
- Run `poetry run pytest tests/e2e/ --collect-only` to verify discovery

### Test Explorer Missing
- This is a known limitation in Cursor
- Use Command Palette commands instead
- Or install Test Explorer UI extension

### Debugging Issues
- Ensure test server starts (check terminal output)
- Verify port 8000 is available
- Check test database permissions

## Alternative: Use VS Code for Test Explorer

If you need full Test Explorer functionality:
1. Open the same project in VS Code
2. VS Code has full Test Explorer support
3. Tests will work the same way
