from playwright.sync_api import expect

from tests_e2e.pages.account import AccountPage
from tests_e2e.pages.math_calculate_solution import MathCalculateSolutionPage
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import POMBaseTest


class TestProfile(POMBaseTest):
    """Test account page."""

    fixtures = ['tests_e2e/fixtures/fixture-db-user.json']

    def setUp(self):
        host = str(self.live_server_url)
        authorize_the_page(self.page, host)
        self.profile = AccountPage(self.page)
        self.profile.navigate(url=f'{host}/users/2/account')

    def test_mult_table_page(self):
        """Test click button for start Table mult exercise."""
        self.profile.mult_table_btn.click()
        self.profile.test_title(MathCalculateSolutionPage.title)

    def test_page_content(self):
        """Test user pofile page content."""
        # The user profile page contains the text of the username.
        expect(self.profile.page.get_by_text('test-user')).to_be_visible()
