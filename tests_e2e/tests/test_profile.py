"""E2E test profile page module."""

from unittest import skip

from playwright.sync_api import expect

from tests_e2e.pages.account import ProfilePage
from tests_e2e.pages.math_calculate_solution import MathCalculateSolutionPage
from tests_e2e.tests.base import POMTest, UserMixin


class TestProfile(UserMixin, POMTest):
    """Test account page."""

    user_name = 'test-user'

    @classmethod
    def setUpClass(cls) -> None:
        """Set up database data."""
        super().setUpClass()
        cls.user = cls.create_user(username=cls.user_name)

    def setUp(self) -> None:
        """Set up page data."""
        super().setUp()
        self.test_page = ProfilePage(self.page, self.host)
        self.page_path = f'/users/{self.user.pk}/account'
        self.authorize_test_page(username=self.user_name)

    @skip
    def test_mult_table_page(self) -> None:
        """Test click button for start Table mult exercise."""
        self.test_page.start_study_mult_table()
        self.test_page.test_title(MathCalculateSolutionPage.title)

    def test_page_content(self) -> None:
        """Test user pofile page content."""
        # The user profile page contains the text of the username.
        self.test_page.navigate(url=self.page_url)
        expect(self.test_page.page.get_by_text(self.user_name)).to_be_visible()
