"""
Example: Using Appium Inspector to identify and interact with elements.

This example shows how to:
1. Launch Inspector to find element locators
2. Use the discovered locators in your test code
3. Verify the element properties
"""

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

capabilities = {
    "platformName": "android",
    "appium:automationName": "uiautomator2",
    "appium:platformVersion": "14",
    "appium:deviceName": "emulator-5554",
    "appium:app": "/path/to/ApiDemos-debug.apk",
    "appium:appPackage": "io.appium.android.apis",
    "appium:appActivity": "io.appium.android.apis.ApiDemos"
}

appium_server_url = 'http://localhost:4723'


def test_find_and_click_element():
    """
    Workflow:
    1. Launch Inspector: python3 -m src.main.utils.appium_inspector_launcher
    2. Click "API Demos" text in the app
    3. Note the locator from Inspector: new UiSelector().text("API Demos")
    4. Use the locator in your test code (as shown below)
    """
    
    # Initialize driver
    load_capabilities = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote(appium_server_url, options=load_capabilities)
    
    try:
        # Use locator discovered in Inspector
        locator = 'new UiSelector().text("API Demos")'
        
        # Wait for element to be visible (Selenium + Appium)
        element = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, locator)
            )
        )
        
        # Verify element properties
        assert element.is_displayed(), "Element should be displayed"
        assert element.is_enabled(), "Element should be enabled"
        
        # Click the element
        element.click()
        
        print("✓ Successfully found and clicked element")
        
    finally:
        driver.quit()


def test_find_element_by_resource_id():
    """
    Another example using Resource ID (discovered in Inspector).
    
    Steps:
    1. Launch Inspector
    2. Click the target element
    3. Look for "Resource ID" in Inspector's element panel
    4. Copy and use in test
    """
    
    load_capabilities = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote(appium_server_url, options=load_capabilities)
    
    try:
        # Using resource ID discovered in Inspector
        locator = 'new UiSelector().resourceId("io.appium.android.apis:id/button")'
        
        element = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, locator)
            )
        )
        
        element.click()
        print("✓ Successfully clicked element by resource ID")
        
    finally:
        driver.quit()


def test_scroll_to_element():
    """
    Example showing how to scroll to find an element.
    
    Use Inspector to:
    1. Verify the element exists but isn't visible
    2. Check that the parent is scrollable
    3. Use UiScrollable to scroll into view
    """
    
    load_capabilities = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote(appium_server_url, options=load_capabilities)
    
    try:
        # Scroll to element using UiScrollable
        # Discovered from Inspector: parent container is scrollable
        locator = (
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector().text("Item Name"))'
        )
        
        element = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, locator)
            )
        )
        
        print("✓ Successfully scrolled to and found element")
        
    finally:
        driver.quit()


if __name__ == "__main__":
    print("Example: Using Appium Inspector for element discovery")
    print("\nBefore running this example:")
    print("1. Start Appium server: appium")
    print("2. Start Android emulator with desired API level")
    print("3. Launch Inspector: python3 -m src.main.utils.appium_inspector_launcher")
    print("4. Use Inspector to identify element locators")
    print("5. Update the locators in this file with your discovered values")
    print("\nThen run this script to test the locators")
