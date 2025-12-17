import unittest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from src.main.utils.wait_till import wait_till

capabilities = {
    "platformName": "android",
    "appium:automationName": "uiautomator2",
    "appium:platformVersion": "16",
    "appium:deviceName": "emulator-5554",
    "appium:app": "/Users/gauravsingh/self/android-apidemos/apks/ApiDemos-debug.apk",
    "appium:appPackage": "io.appium.android.apis",
    "appium:appActivity": "io.appium.android.apis.ApiDemos"
}

appium_server_url = 'http://localhost:4723'


class HideKeyboardTest(unittest.TestCase):
    """
    Test class to verify that the keyboard can be hidden after being shown.
    """

    def setUp(self) -> None:
        load_capabilities = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(appium_server_url, options=load_capabilities)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_keyboard_can_be_hidden(self) -> None:
        views_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Views")')
        views_button.click()

        element_to_find_locator = 'new UiSelector().text("TextFields")'
        scrollable_parent_locator = 'new UiScrollable(new UiSelector().scrollable(true).instance(0))'
        uiautomator_string = f"{scrollable_parent_locator}.scrollIntoView({element_to_find_locator})"

        # Find the element by scrolling it into view
        try:
            target_element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, uiautomator_string)
            print(f"Element '{target_element.text}' scrolled into view and found.")
            # Now you can interact with target_element
        except Exception as e:
            print(f"Error scrolling to element: {e}")

        WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR,
                                                                               'new UiSelector().text("TextFields")')))
        text_fields_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                      'new UiSelector().text("TextFields")')
        text_fields_button.click()
        text_textbox = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("io.appium.android.apis:id/edit1")')))
        text_textbox.click()

        wait_till(True, self.driver.is_keyboard_shown, None)
        self.assertEqual(self.driver.is_keyboard_shown(), True, 'Keyboard is not shown after clicking on text field')

        self.driver.hide_keyboard()
        wait_till(False, self.driver.is_keyboard_shown, None)
        self.assertEqual(self.driver.is_keyboard_shown(), False, 'Keyboard is not hidden')


if __name__ == '__main__':
    unittest.main()
