---
name: appium-inspector-launcher
description: Launch Appium Inspector for element identification in mobile test automation. Use this skill when you need to identify UI element locators, interact with the Android app under test, or debug Appium test selectors. Auto-installs appium-inspector if needed and works cross-platform (macOS, Linux, Windows).
argument-hint: "[--verbose]"
user-invokable: true
---

# Appium Inspector Launcher

This skill launches Appium Inspector, the visual debugging tool for identifying UI elements in mobile applications. Use it when developing or debugging Appium tests to discover element locators and understand the app's UI structure.

## When to use this skill

Use this skill when you need to:
- **Identify element locators** - Find the correct XPath, ID, text, or UiSelector for UI elements
- **Debug test failures** - Visually inspect the app state to understand why a test is failing
- **Explore app structure** - Navigate through the application UI to understand the layout
- **Verify element properties** - Check element attributes, visibility, clickability, and other properties
- **Record interactions** - Capture the exact steps your test should perform
- **Develop new tests** - Use Inspector to identify locators before writing test code

## How it works

1. **Invoke the skill** - Use the `/appium-inspector-launcher` command or the AI agent detects when you need it
2. **Auto-install** - If `appium-inspector` is not installed, it auto-installs via npm (5-minute timeout)
3. **Launch app** - Opens Appium Inspector on your machine (macOS, Linux, or Windows)
4. **Connect to server** - Enter your Appium server URL (typically `http://localhost:4723`)
5. **Start session** - Provide capabilities and click "Start Session" in Inspector
6. **Identify locators** - Interact with the app and identify elements to use in your tests
7. **Copy locators** - Use the locators in your Appium test code

## Setup requirements

Before using this skill, ensure you have:

- **Node.js & npm** - Required for appium-inspector installation [Download](https://nodejs.org/)
- **Appium server running** - On `http://localhost:4723` by default
- **Android emulator or device** - With desired app installed
- **Appium server capabilities** - Know your target platform, device name, and app details

## Command line usage

### Basic launch
```bash
python3 -m src.main.utils.appium_inspector_launcher
```

### With verbose debugging
```bash
python3 -m src.main.utils.appium_inspector_launcher --verbose
```

### Using helper script
```bash
python3 scripts/launch_inspector.py
```

## Programmatic usage

Import and use in your test code:

```python
from src.main.utils.appium_inspector_launcher import AppiumInspectorLauncher

# Basic usage
launcher = AppiumInspectorLauncher()
success = launcher.launch()

# With verbose output for debugging
launcher = AppiumInspectorLauncher(verbose=True)
success = launcher.launch()
```

### Integration with test fixtures

Launch Inspector automatically when tests start:

```python
import unittest
from scripts.launch_inspector import launch_inspector

class MyAppiumTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Auto-launch Inspector when test class starts
        launch_inspector(verbose=True)

    def test_app_functionality(self):
        # Your test code here
        pass
```

## Step-by-step Inspector workflow

### 1. Start Inspector
```bash
python3 -m src.main.utils.appium_inspector_launcher
```

### 2. Configure capabilities

Fill in the Inspector UI with your test configuration:

```json
{
  "platformName": "android",
  "appium:automationName": "uiautomator2",
  "appium:platformVersion": "14",
  "appium:deviceName": "emulator-5554",
  "appium:app": "/path/to/ApiDemos-debug.apk",
  "appium:appPackage": "io.appium.android.apis",
  "appium:appActivity": "io.appium.android.apis.ApiDemos"
}
```

### 3. Click "Start Session"

Inspector connects to your Appium server and app.

### 4. Identify locators

Click elements in the app to see their properties in the Inspector panel. Inspector shows:
- Element text
- Resource ID
- Class name
- Content description
- Accessibility ID
- XPath
- UiSelector (for Android)

### 5. Copy and use locators

From the element properties, copy the locator and add to your test:

```python
from appium.webdriver.common.appiumby import AppiumBy

# Using UiSelector (recommended for Android - best performance)
element = driver.find_element(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("API Demos")'
)

# Or using ID
element = driver.find_element(AppiumBy.ID, "resource_id_here")

# Or using XPath
element = driver.find_element(AppiumBy.XPATH, "//your/xpath/here")
```

## Locator strategy recommendations

For Android apps using uiautomator2:

**Best** - UiSelector (native performance)
```python
locator = 'new UiSelector().text("Button Text")'
element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, locator)
```

**Good** - Resource ID (unique, stable)
```python
locator = 'new UiSelector().resourceId("io.appium.android.apis:id/button")'
element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, locator)
```

**Acceptable** - Scrollable containers
```python
locator = 'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(new UiSelector().text("Item"))'
element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, locator)
```

**Use with caution** - XPath (slower, brittle)
```python
locator = '//android.widget.Button[@content-desc="My Button"]'
element = driver.find_element(AppiumBy.XPATH, locator)
```

Reference: [UiSelector documentation](https://github.com/appium/appium-uiautomator2-driver/blob/master/docs/uiautomator-uiselector.md)

## Troubleshooting

### npm not found error
```
Error: npm is not installed or not in PATH
```

**Solution**: Install Node.js from https://nodejs.org/

### Installation timeout
```
Error: Installation timed out
```

**Solution**: Check your internet connection and try again. Installation normally takes 1-2 minutes.

### Inspector doesn't launch on Linux
```
Error: Executable not found
```

**Solution**: Ensure you have display server available:
```bash
export DISPLAY=:0
python3 -m src.main.utils.appium_inspector_launcher
```

### Inspector doesn't launch on Windows
```
Error: Failed to launch
```

**Solution**: Run from PowerShell or CMD with administrative privileges:
```powershell
python -m src.main.utils.appium_inspector_launcher
```

### Appium server connection fails
If Inspector shows "Connection refused" when starting a session:

1. Verify Appium server is running: `appium --version`
2. Check server is on `http://localhost:4723`
3. Verify firewall allows localhost connections
4. Try: `curl http://localhost:4723/status`

## Related files and documentation

- [Implementation details](../../../docs/APPIUM_INSPECTOR_LAUNCHER.md) - Comprehensive documentation
- [Launcher module](../../../src/main/utils/appium_inspector_launcher.py) - Python source code
- [Helper script](../../../scripts/launch_inspector.py) - Quick launch wrapper
- [Appium documentation](https://appium.io/docs/en/latest/) - Official Appium docs
- [UIAutomator2 guide](https://github.com/appium/appium-uiautomator2-driver) - UiSelector reference

## Example: Finding a button and clicking it

### Using Inspector:
1. Launch Inspector with this skill
2. Click the button you want to interact with
3. Note the `text` property: "Submit"
4. Copy the UiSelector

### In your test code:
```python
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Find and click the button
locator = 'new UiSelector().text("Submit")'
element = WebDriverWait(driver, 10).until(
    ec.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, locator))
)
element.click()
```

## Platform support

The launcher works across all major platforms:

| OS | Method | Status |
|---|---|---|
| macOS | `open -a "Appium Inspector"` | ✅ Fully supported |
| Linux | Execute binary directly | ✅ Fully supported |
| Windows | Execute `.cmd` wrapper | ✅ Fully supported |

## Integration with test development workflow

1. **Develop test** → Open terminal
2. **Run skill** → `/appium-inspector-launcher` or `python3 scripts/launch_inspector.py`
3. **Identify elements** → Click in Inspector to find locators
4. **Copy locators** → Add to your test code
5. **Run tests** → `python3 -m unittest src.tests.android.uiautomator2.test_*`
6. **Debug failures** → Repeat steps 2-4 as needed
