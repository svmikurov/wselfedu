"""The Page Object Model test base class module."""

import os
from typing import Generator

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright

from tests_e2e.pages.user import authorize_the_page
from users.models import UserModel

load_dotenv('./.env_vars/.env')

ENVIRONMENT = os.getenv('ENVIRONMENT')
"""The current environment name (`str`).
"""


class PageFixtureTestCase(StaticLiveServerTestCase):
    """Use Playwright page fixture with StaticLiveServerTestCase.

    The page fixture is set in the test function scope.
    """

    @pytest.fixture(autouse=True)
    def run_around_tests(self) -> Generator[None, None, None]:
        """Get new Playwright Pytest page fixture."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        yield
        self.browser.close()
        self.playwright.stop()

    @classmethod
    def setUpClass(cls) -> None:
        """Allow Django to use async in class scope.

        Sets ``DJANGO_ALLOW_ASYNC_UNSAFE`` to `true`, which allows
        Django to use async at class scope.
        """
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        super().setUpClass()

    @property
    def site_host(self) -> str:
        """Page host schema."""
        return self.live_server_url


class POMTest(PageFixtureTestCase):
    """Base class for testing Page Object Model instance page.

    Example
    -------
    Use to get an authorized page:

    .. code-block:: python

       from tests_e2e.pages.user import authorize_the_page

       class TestPage(POMTest):

          fixtures = ['tests_e2e/fixtures/fixture-db-user']

          def setUp(self):
              authorize_the_page(self.page, self.live_server_url)

    """
