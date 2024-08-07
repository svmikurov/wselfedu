"""Test navbar module."""

from playwright.sync_api import expect

from tests_e2e.pages.home import HomePage
from tests_e2e.pages.navbar import NavbarPageComponent
from tests_e2e.tests.base import POMTest


class TestNavbarPageComponent(POMTest):
    """Test navbar page component."""

    fixtures = ['tests_e2e/fixtures/fixture-db-user.json']

    def setUp(self):
        """Set up test data."""
        super().setUp()
        host = str(self.live_server_url)
        self.home_page = HomePage(self.page, host=host)
        self.navbar = NavbarPageComponent(self.page)

    def test_tutorial_link(self):
        """Test tutorial link."""
        self.home_page.navigate()
        self.navbar.expand_menu()
        expect(self.navbar.tutorial_link).to_be_visible()
