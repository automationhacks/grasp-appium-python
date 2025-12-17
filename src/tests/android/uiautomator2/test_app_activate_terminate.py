import unittest
from time import sleep

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


class AppActivateTerminateTest(unittest.TestCase):
    """
    Test class to verify app activate and terminate functionality.
    """
    def setUp(self) -> None:
        load_capabilities = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(appium_server_url, options=load_capabilities)

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_dialog_text_is_correct(self) -> None:
        wait_till(True, 10, 2, 0.5, self.is_api_demos_installed, None)
        is_app_installed = self.is_api_demos_installed()
        self.assertEqual(is_app_installed, True, 'Oh oh, app is not installed?')

        self.driver.terminate_app('io.appium.android.apis')
        WebDriverWait(self.driver, 10).until(
            ec.invisibility_of_element((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("API Demos")')))

        self.driver.activate_app('io.appium.android.apis')
        WebDriverWait(self.driver, 10).until(
            ec.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("API Demos")')))

        elem = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("API Demos")')
        self.assertEqual(elem.is_displayed(), True)

    def is_api_demos_installed(self) -> bool:
        return self.driver.is_app_installed("io.appium.android.apis")


if __name__ == '__main__':
    unittest.main()
