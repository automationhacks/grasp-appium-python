# grasp-appium-python

## Overview

This project provides examples on how appium can be used to automate an android/iOS app

## Context

- Appium supports different drivers, plugins and clients, depending on your use case, you may want to take a look
  at [Appium docs](https://appium.io/docs/en/latest/ecosystem/)
- Different Appium API methods can be found in docs [here](https://appium.readthedocs.io/en/stable/en/commands/README/)

## Setup

- This project uses python `uv` as the python package manager, to install it run:

```commandline
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Followed by:

```aiignore
uv pip install
```

This should install dependencies specified in pyproject.toml file

```aiignore
npm install -g appium 
```

Other pre-requisites to run the test

- Android studio installed
- ANDROID_HOME setup done
- JAVA_HOME setup done
- AVD (Android virtual device) open with desired API levels
- If real device, developer options enabled with USB debugging enabled
- Install Appium inspector

## Application under test (AUT)

- We'll use Android API demo's app maintained in appium project. You can find the
  repo [here](https://github.com/appium/android-apidemos). After cloning, open this project in Android studio and then
  build the app, you'll see the APK file in `apks/ApiDemos-debug.apk` which can be used to install on a test emulator

## Testing process

- Identify test steps
- Open Appium inspector and update below payload to start an Appium inspection session, here i'm assuming that you
  already have an emulator created with Android 16 version

```aiignore
{
  "platformName": "android",
  "appium:automationName": "uiautomator2",
  "appium:platformVersion": "16",
  "appium:deviceName": "emulator-5554",
  "appium:app": "<path_to_cloned_repo>/android-apidemos/apks/ApiDemos-debug.apk",
  "appium:appPackage": "io.appium.android.apis",
  "appium:appActivity": "io.appium.android.apis.ApiDemos"
}
```

- After this, you can interact with your application and then identify the element you require

See a hello world case that launches the app and verifies if the main screen is displayed
for [test_app_opens.py](src/tests/android/uiautomator2/test_app_opens.py)

## Appium recipes

- [test_current_activity.py](src/tests/android/uiautomator2/test_current_activity.py) shows use of Appium Service to
  start Appium service, get a driver instance and then get current activity of the app
- [App install and uninstall](src/tests/android/uiautomator2/test_app_install_uninstall.py) uninstalls and installs the
  app
- [App launch and close](src/tests/android/uiautomator2/test_app_activate_terminate.py) launches and closes the app
  while checking for the app state as well
- [Check if keyboard is shown and hide it](src/tests/android/uiautomator2/test_hide_keyboard.py)
- [Push a file to device and pull it back](src/tests/android/uiautomator2/test_push_pull_file.py)
- [Change device rotation between portrait and landscape](src/tests/android/uiautomator2/test_device_rotation.py)
- [Change device network connection state](src/tests/android/uiautomator2/test_network_connection.py)
- [Change device location](src/tests/android/uiautomator2/test_change_device_location.py)
- [Take screenshot](src/tests/android/uiautomator2/test_take_screenshot.py)

## Appium actions

- tap
- [scroll](src/tests/android/uiautomator2/test_scroll_and_type_text_in_textbox.py) shows how to use Android `UiScrollable` to scroll to an element
- enter_text
- [drag_and_drop](src/tests/android/uiautomator2/test_long_press_and_drag_and_drop.py) shows how to long press and then
  drag and drop a UI component using ActionChains class

### Checks

- displayed
- selected
- scrollable
- long clickable
- focussed
- focusable
- enabled
- clickable
- checked
- checkable

## Selector/Locators

### Android

- `UiSelector`:
  Read [this](https://github.com/appium/appium-uiautomator2-driver/blob/master/docs/uiautomator-uiselector.md) guide to
  see how UiSelector can be used to find element by text or scroll, its performance is quite close to native