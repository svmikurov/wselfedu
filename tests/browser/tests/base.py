"""Base test for POM browser testing."""

import os
from typing import Generic, Type, TypeVar

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from tests.browser.pages.base import BasePage

T = TypeVar('T', bound=BasePage)


class BaseTest(StaticLiveServerTestCase, Generic[T]):
    """Base test for POV browser testing."""

    playwright: Playwright
    browser: Browser
    _page: Page

    page_type: Type[T]

    @classmethod
    def setUpClass(cls) -> None:
        """Set browser."""
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        """Close browser."""
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self) -> None:
        """Set up page with base url."""
        self._page = self.browser.new_page(
            base_url=str(self.live_server_url),
        )
