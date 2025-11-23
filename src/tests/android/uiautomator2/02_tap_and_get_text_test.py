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

    def test_dialog_text_is_correct(self) -> None:
        elem = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("App")')
        elem.click()

        elem = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Alert Dialogs")')
        elem.click()

        elem = self.driver.find_element(AppiumBy.ID, 'io.appium.android.apis:id/two_buttons')
        elem.click()

        alert_title_elem = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/alertTitle")')))
        if alert_title_elem.is_displayed():
            dialog_text = alert_title_elem.get_attribute('text')
            self.assertIn('Lorem ipsum dolor sit', dialog_text)
        else:
            self.assertEqual(alert_title_elem.is_displayed(), True, 'Alert title dialogue is not visible')


if __name__ == '__main__':
    unittest.main()
