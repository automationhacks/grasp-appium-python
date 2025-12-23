import pathlib
import tempfile

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy

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


def test_get_page_source(appium_service, android_driver_factory):
    custom_opts = {'appium:app': '/Users/gauravsingh/self/android-apidemos/apks/ApiDemos-debug.apk',
                   'appium:deviceName': DEVICE_NAME}
    with android_driver_factory(custom_opts) as driver:
        elem = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("App")')
        elem.click()

        elem = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Alert Dialogs")')
        elem.click()

        with tempfile.TemporaryDirectory() as temp_dir:
            page_source_path = pathlib.Path(temp_dir) / 'page_source.txt'
            print(f'Page source path: {page_source_path}')
            source = driver.page_source
            with open(page_source_path, 'w') as f:
                f.write(source)

            assert page_source_path.is_file() and page_source_path.exists()
