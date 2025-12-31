"""Test login page."""

from playwright.sync_api import expect

from apps.users.models import Person

from ..pages.home import HomePage
from ..pages.login import LoginPage
from .base import BaseTest

USERNAME = 'test_user'
PASSWORD = 'test_pass123'
REDIRECT_TITLE = HomePage.title


class TestLoginPage(BaseTest):
    """Browser testing of the login page."""

    page_type = LoginPage

    def setUp(self) -> None:
        """Create user."""
        # Set up page with base url
        super().setUp()

        self.user = Person.objects.create_user(
            username=USERNAME,
            password=PASSWORD,
        )

        # Create testing page
        self.login_page = LoginPage(self._page)

        # Open page
        self.login_page.open()

    def test_page_title(self) -> None:
        """Test page title."""
        expect(self._page).to_have_title(self.login_page.title)

    def test_login(self) -> None:
        """Test login action."""
        # Act
        self.login_page.login(USERNAME, PASSWORD)

        # Check redirect to Home page on success login
        expect(self._page).to_have_title(REDIRECT_TITLE)
