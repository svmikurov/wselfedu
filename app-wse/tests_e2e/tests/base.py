import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright


class PageTestCase(StaticLiveServerTestCase):
    """Test with Playwright page class.

    Example:
    --------
    from tests_e2e.pages.home import HomePage

    class TestHomePage(PageTestCase):

        def test_home_page(self):
            home_page = HomePage(self.page)
    """

    @classmethod
    def setUpClass(cls):
        """Start Playwright page."""
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()
        cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        """Stop Playwright page."""
        super().tearDownClass()
        cls.browser.close()
        cls.playwright.stop()
