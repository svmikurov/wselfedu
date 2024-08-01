from tests_e2e.pages.account import AccountPage
from tests_e2e.pages.math_calculate_solution import MathCalculateSolutionPage
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import POMBaseTest


class TestAccount(POMBaseTest):
    """Test account page."""

    fixtures = ['tests_e2e/fixtures/fixture-db-user.json']

    def setUp(self):
        host = str(self.live_server_url)
        authorize_the_page(self.page, host)
        self.test_page = AccountPage(self.page)
        self.test_page.navigate(url=f'{host}/users/2/account')

    def test_mult_table_page(self):
        """Test click button for start Table mult exercise."""
        self.test_page.mult_table_btn.click()
        self.test_page.test_title(MathCalculateSolutionPage.title)
