"""The Page Object Model test base class module."""

import os
from typing import Generator
from urllib.parse import urljoin

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright

from config.constants import IS_TEST
from tests_e2e.pages.user import authorize_the_page
from users.models import UserApp

load_dotenv('./.env_vars/.env')

ENVIRONMENT = os.getenv('ENVIRONMENT')
"""The current environment name (`str`).
"""


class PageFixtureTestCase(StaticLiveServerTestCase):
    """Use Playwright page fixture with StaticLiveServerTestCase.

    The page fixture is set in the test function scope.
    """

    page_path = '/'
    """Page path schema, root by default (`str`).
    """
    # host can be set to Django live_server_url or real server
    page_host = None
    """Host of the page being tested (`Optional[str]`).
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
        os.environ[IS_TEST] = 'true'
        super().setUpClass()
        cls.page_host = str(cls.live_server_url)

    @property
    def page_url(self) -> str:
        """Testing page url (`str`, reade-only)."""
        return urljoin(self.page_host, self.page_path)


class UserMixin:
    """Use user in tests methods with mixin.

    Examples
    --------

    .. code-block:: python

        class TestMentorshipProfilePage(UserMixin, POMTest):

        @classmethod
        def setUpClass(cls) -> None:
            super().setUpClass()
            cls.student = cls.create_user(username='student')

        def setUp(self) -> None:
            super().setUp()
            self.test_page = MentorshipProfilePage(self.page, self.host)
            self.page_path = f'/users/mentorship/{self.student.pk}'

        def test_(self) -> None:
            self.authorize_test_page(username='student')
            self.test_page.navigate(url=self.url)
            ...

    """

    page: Page
    """Playwright page instance fixture (`Page`).
    """
    page_host: str
    """Host of the page being tested (`str`).
    """

    @staticmethod
    def create_user(username: str) -> UserApp:
        """Create user."""
        return UserApp.objects.create_user(
            username=username, password='1q2s3d4r'
        )

    def authorize_test_page(self, username: str) -> None:
        """Authorize the testing page instance."""
        authorize_the_page(
            page=self.page,
            host=self.page_host,
            user_name=username,
            user_pass='1q2s3d4r',
        )


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
