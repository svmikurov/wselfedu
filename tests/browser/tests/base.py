"""Base Playwright POM test."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Page, Playwright


class BaseTest(StaticLiveServerTestCase):
    """Base Playwright POM test."""

    playwright: Playwright
    browser: Browser
    _page: Page

    @classmethod
    def setUpClass(cls) -> None:
        """Start the Playwright and launch the browser."""
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the playwright and close the browser."""
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self) -> None:
        """Set up page with base url."""
        self._page = self.browser.new_page(base_url=str(self.live_server_url))
