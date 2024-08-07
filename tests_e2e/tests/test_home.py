"""The home page representation test module."""
from urllib.parse import urljoin

from tests_e2e.pages.home import HomePage
from tests_e2e.tests.base import POMTest


class TestHomePage(POMTest):
    """Test home page class."""

    def setUp(self) -> None:
        """Set up test data."""
        self.home_page = HomePage(self.page)
        url = urljoin(self.live_server_url, self.home_page.path)
        self.home_page.navigate(url=url)

    def test_home_page(self) -> None:
        """Test home page title."""
        self.home_page.test_title(HomePage.title)
