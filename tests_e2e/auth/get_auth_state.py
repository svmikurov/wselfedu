"""Save storage state for Playwright tests module.

See Also
--------
   * Playwright: `reusing signed in state <https://playwright.dev/python/docs/auth#reusing-signed-in-state>`_

"""  # noqa: E501

import os

from dotenv import load_dotenv

from tests_e2e.pages.home import HomePage
from tests_e2e.pages.user import LoginPage
from tests_e2e.tests.base import POMBaseTest

load_dotenv('./.env_vars/.env.wse')

USER_NAME = os.getenv('TEST_USER_NAME')
"""Username, typically used by default in tests and fixtures.
"""
USER_PASS = os.getenv('TEST_USER_PASS')
"""User password, typically used by default in tests and fixtures.
"""
STATE_PATH = 'tests_e2e/auth/state.json'
"""Path to saved storage state.
"""


class TestGetAuthState(POMBaseTest):
    """Get auth state class."""

    def test_get_auth_state(self) -> None:
        """Get auth state."""
        login_page = LoginPage(self.page)
        login_page.navigate(url=f'{self.site_host}{login_page.path}')
        login_page.test_title()
        login_page.login(USER_NAME, USER_PASS)
        login_page.test_title(expected_title=HomePage.title)

        self.page.context.storage_state(path=STATE_PATH)
