"""The Page Object Model module of base page test."""

import os
from typing import Generator, Optional
from urllib.parse import urljoin

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import Page, expect, sync_playwright

from tests.tests_plw.pages.home import HomePage
from tests.tests_plw.pages.login import LoginPage
from users.models import UserModel


class BaseTest(StaticLiveServerTestCase):
    """Base test page of Page Object Model.

    .. seealso::

        * `StaticLiveServerTestCase <https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#specialized-test-case-to-support-live-testing>`_

    """  # noqa: E501

    page_path = '/'
    """Page path schema, root by default (`str`).
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
    def page_url(self) -> str:
        """Testing page url (`str`, reade-only)."""
        return urljoin(self.page_host, self.page_path)

    @property
    def page_host(self) -> str:
        """Host of the page being tested (`str`, reade-only)."""
        return str(self.live_server_url)


class UserMixin:
    """Use user in tests methods with mixin."""

    page: Page
    """Playwright Pytest page fixture (`Page`)
    """
    page_host: str
    """Host of the page being tested (`Optional[str]`).
    """
    page_path: str
    """Page path schema (`str`).
    """
    page_url: str
    """Testing page url (`str`).
    """
    user: Optional[UserModel]
    """User by default (`Optional[UserModel]`)
    """
    password = '1q2s3d4r'
    """All created users have a single password (`str`).
    """

    def create_user(
        self,
        username: Optional[str] = None,
    ) -> Optional[UserModel]:
        """Create user.

        Return user instance if given ``username`` parameter,
        create ``user`` class attribute otherwise.
        All created users have a single password.

        Parameters
        ----------
        username : `str`, optional
            The name of created user. ``user`` by default.

        Return
        ------
        user : `UserModel` | None
            The user model instance if given ``username`` parameter,
            None otherwise and create ``user`` class attribute.

        """
        user = UserModel.objects.create_user(
            username=username or 'user',
            password='1q2s3d4r',
        )

        if username:
            return user
        else:
            self.user = user

    def authorize_test_page(self, user: UserModel = None) -> None:
        """Authorize the testing page instance.

        Parameters
        ----------
        user : `UserModel`, optional
            The instance of the user model under which the system is
            logged in. ``self.user`` by default.

        """
        user = user or self.user
        login_page = LoginPage(self.page)
        self.page_path = login_page.path
        login_page.navigate(page_url=self.page_url)
        login_page.login(user.username, self.password)
        expect(login_page.page).to_have_title(HomePage.title)


class POMTest(
    BaseTest,
    UserMixin,
):
    """Class representing the testing page with general tests.

    Inherit your test classes from this class.

    .. _pom_test_example:

    Example
    -------
    .. code-block:: python

        TestClass(POMTest):

        username = 'Sasha'

        def setUp(self) -> None:
            super().setUp()
            self.user = self.create_user(username=self.username)
            self.test_page = PageClass(self.page)
            self.authorize_test_page(user=self.user)
            self.page_path = f'/users/profile/{self.user.pk}'
            self.test_page.navigate(page_url=self.page_url)

        def test_odo_ne(self) -> None:
            self.test_page.do_one()
            expect(self.text_page.locator_one).to_have_text('one')

        def test_do_two(self) -> None:
            self.test_page.do_two()
            expect(self.text_page.locator_two).to_have_text('two')

    """
