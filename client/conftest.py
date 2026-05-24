import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config.config import Config
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.fixture(scope='function')
def driver():
    """Provides a fresh browser per test function."""
    browser = Config.BROWSER.lower()

    if browser == 'chrome':
        options = webdriver.ChromeOptions()
        if Config.HEADLESS:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1280,900')
        service = ChromeService(ChromeDriverManager().install())
        drv = webdriver.Chrome(service=service, options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument('--headless')
        service = FirefoxService(GeckoDriverManager().install())
        drv = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    drv.implicitly_wait(Config.TIMEOUT)
    yield drv
    drv.quit()


@pytest.fixture(scope='function', autouse=True)
def screenshot_on_failure(driver, request):
    """Auto-capture screenshot when a test fails."""
    yield
    # Check if the test failed
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        name = request.node.name.replace(' ', '_')
        screenshot_dir = 'reports/screenshots'
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        driver.save_screenshot(os.path.join(screenshot_dir, f'{name}.png'))


# Make rep_call available to screenshot_on_failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


@pytest.fixture(scope='function')
def auth_session(driver):
    LoginPage(driver).open().login(
        Config.VALID_USERNAME, Config.VALID_PASSWORD,
    )
    dash = DashboardPage(driver)
    dash.wait_for_url('/dashboard')
    assert dash.is_loaded(), 'Dashboard title not visible'

    yield driver
