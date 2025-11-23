import unittest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

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


class AppLaunchTest(unittest.TestCase):
    def setUp(self) -> None:
        load_capabilities = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(appium_server_url, options=load_capabilities)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def type_text_in_textbox_test(self) -> None:
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

        text_fields_button = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("TextFields")')
        text_fields_button.click()

        text_textbox = self.driver.find_element(AppiumBy.ID, 'new UiSelector().resourceId("io.appium.android.apis:id/edit1")')
        text_to_type = 'Appium UI automator is awesome!'
        text_textbox.send_keys(text_to_type)

        alert_title_elem = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("io.appium.android.apis:id/edit1")')))

        if alert_title_elem.is_displayed():
            dialog_text = alert_title_elem.get_attribute('text')
            self.assertEqual(text_to_type, dialog_text)
        else:
            self.assertEqual(alert_title_elem.is_displayed(), True, 'Alert title dialogue is not visible')


if __name__ == '__main__':
    unittest.main()
