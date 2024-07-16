import os

from dotenv import load_dotenv

from tests_e2e.pages.user import LoginPage
from tests_e2e.tests.base import PageTestCase

load_dotenv()

USER_NAME = os.getenv('TEST_USER_NAME')
USER_PASS = os.getenv('TEST_USER_PASS')
STATE_PATH = 'tests_e2e/auth/state.json'


class TestGetAuthState(PageTestCase):
    """Get auth state class."""

    def test_get_auth_state(self):
        login_page = LoginPage(self.page)
        url = f"{self.live_server_url}{login_page.path}"
        login_page.navigate(url)
        login_page.test_title()
        login_page.login(USER_NAME, USER_PASS)

        self.page.context.storage_state(path=STATE_PATH)
