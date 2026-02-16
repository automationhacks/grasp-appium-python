# Copilot Instructions for grasp-appium-python

## Project Overview

This is a learning repository demonstrating Appium usage for mobile test automation in Python. It contains example test cases for Android automation using the uiautomator2 driver, with the API Demos app as the application under test (AUT).

## Setup & Dependencies

**Package Manager**: `uv` (Python package manager)

**Install dependencies**:
```bash
uv pip install
```

This installs `appium-python-client>=5.2.4` defined in `pyproject.toml`.

**Environment Requirements** (before running tests):
- Appium server installed globally: `npm install -g appium`
- Android Studio with SDK installed
- `ANDROID_HOME` and `JAVA_HOME` environment variables configured
- Android Virtual Device (AVD) running with desired API level
- Application under test (AUT): API Demos APK from [appium/android-apidemos](https://github.com/appium/android-apidemos)
- Appium Inspector (for element locator identification)

## Running Tests

**Note**: Tests are currently implemented using `unittest` (not pytest). The Appium server must be running on `http://localhost:4723` before executing tests.

Tests require an active Android emulator/device and a running Appium server:

```bash
# Terminal 1: Start Appium server (requires npm)
appium

# Terminal 2: Run a single test
python -m unittest src.tests.android.uiautomator2.test_app_opens

# Run all tests in a module
python -m unittest src.tests.android.uiautomator2

# Run all tests in the project
python -m unittest discover -s src/tests -p "test_*.py"
```

## Project Architecture

### Directory Structure
```
src/
├── main/
│   └── utils/
│       └── wait_till.py          # Custom polling utility for element state
└── tests/
    └── android/
        └── uiautomator2/
            ├── base.py            # BaseDriver class with common actions
            ├── test_app_opens.py  # Hello world example
            └── test_*.py          # Individual test recipes
```

### Key Components

**`BaseDriver` class** (`src/tests/android/uiautomator2/base.py`):
- Wraps Appium WebDriver with common actions
- `tap(AppiumBy, locator, timeout)` - Click element with explicit wait
- `find_element(AppiumBy, locator, timeout)` - Find with visibility wait using Selenium's WebDriverWait

**`wait_till()` utility** (`src/main/utils/wait_till.py`):
- Custom polling function for checking conditions with configurable retry behavior
- Parameters: `expected` value, function to call, timeout, initial sleep duration, sleep multiplier

### Test Pattern

All tests follow this structure:
1. Define capabilities dictionary with Appium options (platformName, automationName, platformVersion, deviceName, app, appPackage, appActivity)
2. `setUp()`: Initialize driver via `webdriver.Remote()` with `UiAutomator2Options`
3. `tearDown()`: Quit driver
4. Test methods: Interact with app and assert expected behavior

## Key Conventions

### Capabilities Configuration
- Hardcoded in each test file (not centralized)
- Uses `UiAutomator2Options().load_capabilities(dict)` to load capability dictionaries
- `appium_server_url` typically `http://localhost:4723`

### Element Locators
- **Primary strategy**: `AppiumBy.ANDROID_UIAUTOMATOR` with UiSelector syntax (native Android performance)
  - Example: `'new UiSelector().text("API Demos")'`
  - See [uiautomator-uiselector.md](https://github.com/appium/appium-uiautomator2-driver/blob/master/docs/uiautomator-uiselector.md)

### Wait Strategy
- Use `WebDriverWait` with `expected_conditions.visibility_of_element_located()` for explicit waits
- Default timeout: 10 seconds
- Alternatively use custom `wait_till()` for polling conditions

### Test Organization
- Tests grouped by platform (android/) and driver type (uiautomator2/)
- Each test file demonstrates a specific Appium recipe or capability
- Single test class per file using `unittest.TestCase`

## Agent Skills

### Appium Inspector Launcher

Cross-platform skill to automatically launch Appium Inspector for element identification.

**Usage**:
```bash
# Command line
python3 -m src.main.utils.appium_inspector_launcher

# Or use helper script
python3 scripts/launch_inspector.py

# In Python code
from src.main.utils.appium_inspector_launcher import AppiumInspectorLauncher
launcher = AppiumInspectorLauncher(verbose=True)
launcher.launch()
```

**Features**:
- Auto-installs `appium-inspector` via npm if missing
- Supports macOS, Linux, and Windows
- Programmatic API for test fixtures
- Optional verbose logging

See [APPIUM_INSPECTOR_LAUNCHER.md](../../docs/APPIUM_INSPECTOR_LAUNCHER.md) for detailed documentation.

## Appium Documentation References

- [Appium Ecosystem Drivers](https://appium.io/docs/en/latest/ecosystem/)
- [Appium 2.19 API Commands](https://appium.io/docs/en/2.19/commands/base-driver/#getpagesource)
- [UIAutomator2 Driver Docs](https://github.com/appium/appium-uiautomator2-driver)
