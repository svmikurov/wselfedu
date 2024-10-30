"""The home page representation test module.

Testing using the :obj:`HomePage <tests_plw.pages.home.HomePage>`
page representation class.
"""

from tests_plw.pages import HomePage
from tests_plw.tests.base import POMTest


class TestHomePage(POMTest):
    """Test home page class.

    Test not authorized page.

    .. admonition:: Test what the page contains

        * Page title

    """

    def setUp(self) -> None:
        """Set up test data."""
        self.home_page = HomePage(self.page)
        self.page_path = self.home_page.path
        self.home_page.navigate(page_url=self.page_url)

    def test_home_page(self) -> None:
        """Test home page title."""
        self.home_page.test_title()
