"""The home page representation test module."""

from tests_e2e.tests.base import POMTest
from tests_plw.pages.home import HomePage


class TestHomePage(POMTest):
    """Test home page class."""

    def setUp(self) -> None:
        """Set up test data."""
        self.home_page = HomePage(self.page)
        self.home_page.navigate(page_url=self.page_url)

    def test_home_page(self) -> None:
        """Test home page title."""
        self.home_page.test_title(HomePage.title)
