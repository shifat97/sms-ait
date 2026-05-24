import pytest
from selenium.webdriver.chrome.options import Options

from config.config import Config
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

options = Options()


class TestAuth:
    @pytest.mark.auth
    def test_logout(self, driver):
        """Logout Button → move to the login page"""
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)

        login_page.open()
        login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)

        login_page.wait_for_url(dashboard_page.PATH)
        assert '/dashboard' in dashboard_page.current_url, f"Expected '/dashboard', Got {dashboard_page.current_url}"

        dashboard_page.logout()

        login_page.wait_for_url(login_page.PATH)
        assert '/signin' in login_page.current_url, f"Expected '/signin', Got {login_page.current_url}"

        assert login_page.find(login_page.TITLE).text == 'Sign In', f"Expected signin, Got something else"

    @pytest.mark.auth
    def test_logout_after_ls_clear(self, driver, auth_session):
        """Clear local storage → reload page → move to the sign in page"""
        driver.execute_script("window.localStorage.clear();")
        driver.refresh()

        assert '/signin' in driver.current_url, f"Expected '/signin', Got {driver.current_url}"
