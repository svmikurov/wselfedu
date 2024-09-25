"""Test navbar module."""

from playwright.sync_api import expect

from tests.tests_e2e.pages.navbar import NavbarPageComponent
from tests.tests_e2e.tests.base import POMTest
from tests_plw.pages.home import HomePage


class TestNavbarPageComponent(POMTest):
    """Test navbar page component."""

    fixtures = ['tests/tests_e2e/fixtures/fixture-db-user.json']

    def setUp(self) -> None:
        """Set up test data."""
        super().setUp()
        self.home_page = HomePage(self.page)
        self.navbar = NavbarPageComponent(self.page)

    def test_tutorial_link(self) -> None:
        """Test tutorial link."""
        self.home_page.navigate(page_url=self.page_url)
        self.navbar.expand_menu()
        expect(self.navbar.tutorial_link).to_be_visible()
