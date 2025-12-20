import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.appium_service import AppiumService
from assertpy import assert_that

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
    options.platform_version = '16.0'
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


def test_device_network(appium_service, android_driver_factory):
    """
    Possible values:

            +--------------------+------+------+---------------+
            | Value (Alias)      | Data | Wifi | Airplane Mode |
            +====================+======+======+===============+
            | 0 (None)           | 0    | 0    | 0             |
            +--------------------+------+------+---------------+
            | 1 (Airplane Mode)  | 0    | 0    | 1             |
            +--------------------+------+------+---------------+
            | 2 (Wifi only)      | 0    | 1    | 0             |
            +--------------------+------+------+---------------+
            | 4 (Data only)      | 1    | 0    | 0             |
            +--------------------+------+------+---------------+
            | 6 (All network on) | 1    | 1    | 0             |
            +--------------------+------+------+---------------+
    :param appium_service:
    :param android_driver_factory:
    :return:
    """

    custom_opts = {'appium:app': '/Users/gauravsingh/self/android-apidemos/apks/ApiDemos-debug.apk',
                   'appium:deviceName': 'emulator-5554'}
    with android_driver_factory(custom_opts) as driver:
        driver.set_network_connection(6)
        network_connection = driver.network_connection
        assert_that(network_connection).is_equal_to(6)

        driver.set_network_connection(4)
        network_connection = driver.network_connection
        assert_that(network_connection).is_equal_to(4)

        driver.set_network_connection(2)
        network_connection = driver.network_connection
        assert_that(network_connection).is_equal_to(2)
