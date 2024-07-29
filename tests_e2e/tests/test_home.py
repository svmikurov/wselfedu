"""
The home page representation test module.
"""
from playwright.sync_api import expect

from tests_e2e.pages.home import HomePage
from tests_e2e.pages.tasks.index import IndexTaskPage
from tests_e2e.tests.base import POMBaseTest


class TestHomePage(POMBaseTest):
    """Test home page class."""

    def setUp(self) -> None:
        self.home_page = HomePage(self.page)
        url = f"{self.site_host}{self.home_page.path}"
        self.home_page.navigate(url=url)

    def test_home_page(self) -> None:
        """Test home page title."""
        self.home_page.test_title(HomePage.title)

    def test_all_page_btn(self) -> None:
        expect(self.home_page.all_tasks_btn).to_be_visible()
        self.home_page.all_tasks_btn.click()
        self.home_page.test_title(IndexTaskPage.title)
