"""E2E test profile page module."""

from unittest import skip

from playwright.sync_api import expect

from tests_e2e.pages.account import ProfilePage
from tests_e2e.pages.math_calculate_solution import MathCalculateSolutionPage
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import POMTest
from users.models import UserModel


class TestProfile(POMTest):
    """Test account page."""

    fixtures = ['tests_e2e/fixtures/fixture-db-user.json']

    def setUp(self) -> None:
        """Set up page data."""
        self.host = str(self.live_server_url)
        authorize_the_page(self.page, self.host)
        self.user_id = UserModel.objects.get(username='test-user').pk
        self.profile = ProfilePage(self.page)
        self.url = f'{self.host}/users/{self.user_id}/account'

    @skip
    def test_mult_table_page(self) -> None:
        """Test click button for start Table mult exercise."""
        self.profile.page.goto(url=self.url)
        self.profile.start_study_mult_table()
        self.profile.test_title(MathCalculateSolutionPage.title)

    def test_page_content(self) -> None:
        """Test user pofile page content."""
        self.profile.page.goto(url=self.url)
        # The user profile page contains the text of the username.
        expect(self.profile.page.get_by_text('test-user')).to_be_visible()
