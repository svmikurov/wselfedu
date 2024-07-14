from playwright.sync_api import expect

from tests_e2e.pages.home import HomePage
from tests_e2e.tests.base import PageTestCase


class TestHomePage(PageTestCase):
    """Test home page class."""

    def test_home_page(self):
        """Test home page title."""
        home_page = HomePage(self.page)
        host = self.live_server_url
        home_page.navigate(host)

        expect(self.page).to_have_title(HomePage.title)
