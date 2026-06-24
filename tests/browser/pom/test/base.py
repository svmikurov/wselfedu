"""Base Playwright POM test."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Page, Playwright


class _Test(StaticLiveServerTestCase):
    """Base Playwright POM test.

    Uses the Firefox browser.
    """

    playwright: Playwright
    browser: Browser
    _page: Page

    @classmethod
    def setUpClass(cls) -> None:
        """Start the Playwright and launch the browser."""
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.firefox.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the playwright and close the browser."""
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()


class BaseTest(_Test):
    """Base Playwright POM test for not authenticated user."""

    def setUp(self) -> None:
        """Set up page with base url."""
        self._page = self.browser.new_page(base_url=str(self.live_server_url))
