import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from playwright.sync_api import sync_playwright


class PlaywrightTestCase(StaticLiveServerTestCase):
    """Apply Playwright test this Django tests."""

    @classmethod
    def setUpClass(cls):
        """Start playwright."""
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.base_url = cls.live_server_url
        cls.page = cls.browser.new_page()
        cls.page.goto(cls.base_url)

    @classmethod
    def tearDownClass(cls):
        """Stop playwright."""
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()
