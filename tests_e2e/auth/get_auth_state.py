import os

from dotenv import load_dotenv

from tests_e2e.pages.home import HomePage
from tests_e2e.pages.user import LoginPage
from tests_e2e.tests.base import POMBaseTest

load_dotenv()

USER_NAME = os.getenv('TEST_USER_NAME')
USER_PASS = os.getenv('TEST_USER_PASS')
STATE_PATH = 'tests_e2e/auth/state.json'


class TestGetAuthState(POMBaseTest):
    """Get auth state class."""

    def test_get_auth_state(self) -> None:
        """Get auth state."""
        login_page = LoginPage(self.page)
        login_page.navigate(url=f"{self.site_host}{login_page.path}")
        login_page.test_title()
        login_page.login(USER_NAME, USER_PASS)
        login_page.test_title(expected_title=HomePage.title)

        self.page.context.storage_state(path=STATE_PATH)
