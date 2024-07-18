"""
The home page representation test module.
"""


from tests_e2e.pages.home import HomePage
from tests_e2e.tests.base import POMBaseTest


class TestHomePage(POMBaseTest):
    """Test home page class."""

    def test_home_page(self) -> None:
        """Test home page title."""
        home_page = HomePage(self.page)
        home_page.navigate(url=f"{self.site_host}{home_page.path}")
        home_page.test_title(HomePage.title)
