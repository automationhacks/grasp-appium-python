import unittest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

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

    def test_app_home_page_is_displayed(self) -> None:
        elem = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("API Demos")')
        self.assertEqual(elem.is_displayed(), True)


if __name__ == '__main__':
    unittest.main()
