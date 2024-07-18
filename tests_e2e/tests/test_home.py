from tests_e2e.pages.home import HomePage
from tests_e2e.tests.base import PageTestCase


class TestHomePage(PageTestCase):
    """Test home page class."""

    def test_home_page(self):
        """Test home page title."""
        home_page = HomePage(self.page)
        home_page.navigate(url=f"{self.live_server_url}{home_page.path}")
        home_page.test_title(HomePage.title)
