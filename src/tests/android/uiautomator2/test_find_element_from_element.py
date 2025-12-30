import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'
ANDROID_VERSION = '16.0'
DEVICE_NAME = 'emulator-5554'


@pytest.fixture(scope="session")
def appium_service():
    service = AppiumService()
    service.start(args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT)], timeout_ms=20 * 1000)
    yield service
    service.stop()


def get_android_driver(custom_options=None):
    options = UiAutomator2Options()
    options.platform_version = ANDROID_VERSION
    if custom_options:
        options.load_capabilities(custom_options)
    return webdriver.Remote(f'http://{APPIUM_HOST}:{APPIUM_PORT}', options=options)


@pytest.fixture
def android_driver_factory():
    return get_android_driver


@pytest.fixture
def android_driver():
    driver = get_android_driver()
    yield driver
    driver.quit()


def test_find_element_from_element(appium_service, android_driver_factory):
    custom_opts = {'appium:app': '/Users/gauravsingh/self/android-apidemos/apks/ApiDemos-debug.apk',
                   'appium:deviceName': DEVICE_NAME}
    with android_driver_factory(custom_opts) as driver:
        content_text_view = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Content")')))
        content_text_view.click()

        clipboard_text_view = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Clipboard")')))
        clipboard_text_view.click()

        data_type_text_view = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/text1")')))
        data_type_text_view.click()

        container = WebDriverWait(driver, 10).until(
            ec.visibility_of_element_located(
                (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("android:id/content")')))
        html = container.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("io.appium.android.apis:id/html_text")')
        inner_html = html.get_attribute('text')

        assert inner_html == '<b>Link:</b> <a href="http://www.android.com">Android</a>'
