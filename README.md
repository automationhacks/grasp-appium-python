# grasp-appium-python

## Overview

This project provides examples on how appium can be used to automate an android/iOS app

## Context

- Appium supports different drivers, plugins and clients, depending on your use case, you may want to take a look at [Appium docs](https://appium.io/docs/en/latest/ecosystem/)

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

- We'll use Android API demoes app maintained in appium project. You can find the
  repo [here](https://github.com/appium/android-apidemos). After cloning, open this project in Android studio and then
  build the app, you'll see the APK file in `apks/ApiDemos-debug.apk` which can be used to install on a test emulator

## Testing process

- Identify test steps
- Open Appium inspector and update below payload to start an Appium inspection session, here i'm assuming that you already have an emulator created with Android 16 version

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

## Appium actions

- tap
- scroll
- enter_text

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