"""The base page test class of Page Object Model.

Inherit test classes from the derived **POMTest class** to use the Page
Object Model for tests with general attributes and methods.

Manage environs (by the :py:meth:`setUpClass <BaseTest.setUpClass>`):
    - ``DJANGO_ALLOW_ASYNC_UNSAFE`` environ is `true` - allows Django to
      use async at class scope.
    - ``IS_TEST`` environ is `true` - disables loading bootstrap into
      the page template to speed up tests.
"""

import os
from typing import Generator, Optional
from urllib.parse import urljoin

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import Page, expect, sync_playwright

from config.constants import IS_TEST
from tests_plw.pages.home import HomePage
from tests_plw.pages.login import LoginPage
from users.models import UserApp


class BaseTest(StaticLiveServerTestCase):
    """Base test class to test page of Page Object Model."""

    page_path = '/'
    """Testing page path schema, root by default (`str`).
    """
    page: Page
    """Playwright Pytest page fixture (`Page`).

    Generated by
    :py:meth:`BaseTest.run_around_tests <BaseTest.run_around_tests>`.
    """

    @pytest.fixture(autouse=True)
    def run_around_tests(self) -> Generator[None, None, None]:
        """Generate Playwright Pytest page fixture."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        yield
        self.browser.close()
        self.playwright.stop()

    @classmethod
    def setUpClass(cls) -> None:
        """Set environs.

        Sets ``DJANGO_ALLOW_ASYNC_UNSAFE`` environ is `true`, which
        allows Django to use async at class scope.

        Sets ``IS_TEST`` environ is `true`, this disables loading
        bootstrap into the page template to speed up tests.
        """
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        os.environ[IS_TEST] = 'true'
        super().setUpClass()

    @property
    def page_url(self) -> str:
        """Testing page url (`str`, reade-only)."""
        return urljoin(self.page_host, self.page_path)

    @property
    def page_host(self) -> str:
        """Host of the page being tested (`str`, reade-only).

        Django StaticLiveServerTestCase creates a new host for
        each test.
        """
        return str(self.live_server_url)


class UserMixin:
    """Testing page user mixin."""

    user: Optional[UserApp] = None
    """User by default (`Optional[UserApp]`).
    """
    username = 'user'
    """Username, by default (`str`).
    """
    password = '1q2s3d4r'
    """All created users have a single password (`str`).
    """
    page: Page
    page_url: str
    page_host: str
    page_path: str

    def create_user(self, username: str | None = None) -> UserApp:
        """Create user.

        All created users have a single
        :py:attr:`password <UserMixin.password>`.

        :param str username: Username, "user" by default.
        :return: User instance.
        :rtype: UserApp
        """
        return UserApp.objects.create_user(
            username=username or self.username,
            password=self.password,
        )

    def authorize_test_page(self, user: Optional[UserApp] = None) -> None:
        """Authorize the testing page instance.

        :param UserApp user: The instance of the Django UserApp
         under which the system is logged in,
         :py:attr:`self.user <UserMixin.user>` by default.
        """
        if not user and not self.user:
            self.user = self.create_user()
        auth_user = user or self.user
        login_page = LoginPage(self.page)
        page_path = login_page.path
        page_url = urljoin(self.page_host, page_path)

        login_page.navigate(page_url=page_url)
        login_page.login(auth_user.username, self.password)
        expect(login_page.page).to_have_title(HomePage.title)


class POMTest(BaseTest, UserMixin):
    """Page Object Model test class."""
