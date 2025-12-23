import pytest
import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'


@pytest.fixture(scope="session")
def appium_service():
    service = AppiumService()
    service.start(args=['--address', APPIUM_HOST, '-p', str(APPIUM_PORT)], timeout_ms=20 * 1000)
    yield service
    service.stop()


def get_android_driver(custom_options=None):
    options = UiAutomator2Options()
    options.platform_version = '13.0'
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


# This test does not work, Appium uses adb geo fix method which did not work for Android 16
# Also tested this on android 13 without play services and it does not work there as well.
def test_change_device_geo_location(appium_service, android_driver_factory):
    custom_opts = {'appium:app': '/Users/gauravsingh/self/android-apidemos/apks/ApiDemos-debug.apk',
                   'appium:deviceName': 'emulator-5556'}
    with android_driver_factory(custom_opts) as driver:
        current_location = driver.location
        print(f"Current location: {current_location}")

        lat = 12
        long = 77
        altitude = 10
        driver.set_location(lat, long, altitude)
        time.sleep(10)

        updated_location = driver.location
        print(f"Updated location: {updated_location}")

        assert updated_location.get('latitude') == lat
        assert updated_location.get('longitude') == long
