"""The home page representation test module."""

from tests_e2e.pages.home import HomePage
from tests_e2e.tests.base import POMBaseTest


class TestHomePage(POMBaseTest):
    """Test home page class."""

    def setUp(self) -> None:
        """Set up test data."""
        self.home_page = HomePage(self.page)
        url = f'{self.site_host}{self.home_page.path}'
        self.home_page.navigate(url=url)

    def test_home_page(self) -> None:
        """Test home page title."""
        self.home_page.test_title(HomePage.title)
