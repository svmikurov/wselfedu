from tests_e2e.pages.mathem.math_calculate_choice import \
    MathCalculateChoicePage
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import POMBaseTest


class TestMathCalculateChoicePage(POMBaseTest):
    """Mathematical calculation conditions page test class."""

    fixtures = ['tests_e2e/fixtures/fixture-db-user']

    def setUp(self) -> None:
        """Create page instance."""
        host = str(self.live_server_url)
        self.choice_page = MathCalculateChoicePage(self.page, host=host)
        authorize_the_page(self.page, host)
        self.choice_page.navigate()

    def test_choose_calculation_conditions(self) -> None:
        """Test choose calculation conditions."""
        self.choice_page.test_title()
        self.choice_page.choose_calculation_conditions(
            calculation='+',
            min_value='6',
            max_value='6',
        )
