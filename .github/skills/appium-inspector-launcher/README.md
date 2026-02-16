# Appium Inspector Launcher Skill

This directory contains the **Appium Inspector Launcher** agent skill, which provides automated launching and configuration of Appium Inspector for mobile test automation.

## Files

- **`SKILL.md`** - Agent skill definition with instructions, usage patterns, and troubleshooting
- **`examples/`** - Example code showing how to use Inspector for element discovery
  - `element-discovery-workflow.py` - Step-by-step workflow for finding and using locators
  - `test-integration-pattern.py` - How to integrate Inspector launching in test fixtures

## Quick Start

### For Copilot Users

In VS Code chat, use the skill:
```
/appium-inspector-launcher
```

Or ask Copilot directly:
- "Launch Appium Inspector for my Android app"
- "Help me identify element locators for my test"
- "Debug why my selector isn't finding the element"

### For CLI Users

From the terminal:
```bash
python3 -m src.main.utils.appium_inspector_launcher
```

### For Test Integration

In your test fixtures:
```python
from scripts.launch_inspector import launch_inspector

class MyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        launch_inspector(verbose=True)
```

## What This Skill Does

✅ **Launches Appium Inspector** - Visual UI element inspection tool  
✅ **Auto-installs if needed** - Automatically installs `appium-inspector` via npm  
✅ **Cross-platform** - Works on macOS, Linux, and Windows  
✅ **Provides guidance** - Step-by-step instructions for element discovery  
✅ **Shows best practices** - Recommends optimal locator strategies  

## When to Use

- Discovering element locators for your Appium tests
- Debugging test failures with visual inspection
- Exploring app UI structure and hierarchy
- Verifying element properties and states
- Developing new test cases with element discovery

## Learn More

See `SKILL.md` for:
- Detailed setup requirements
- Complete workflow instructions
- Locator strategy recommendations
- Troubleshooting guide
- Integration patterns

See `examples/` for:
- Real-world element discovery workflow
- Test fixture integration patterns
- Different locator strategies (UiSelector, ID, XPath)
- Scrolling and interaction examples

## Requirements

- **Node.js & npm** - For appium-inspector installation
- **Appium server** - Running on http://localhost:4723
- **Android emulator or device** - With your app installed
- **Python 3.13+** - For the launcher script

## Agent Skills Standard

This skill follows the [Agent Skills open standard](https://agentskills.io) and works with:
- GitHub Copilot in VS Code
- GitHub Copilot CLI
- GitHub Copilot coding agent
