from unittest import skip

from playwright.sync_api import expect

from tests_e2e.pages.math_calculate_choice import (
    MathCalculateChoicePage,
)
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import POMBaseTest


@skip('Tests are not stable. The expected page uses ajax.')
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
            calculation='add',
            time_answer='1',
            min_value='5',
            max_value='6',
            input_answer_choice=False,
        )
        expect(
            self.page.locator('#question_text')
        ).to_contain_text('5 + 6', timeout=20000)

    def test_choose_calculation_conditions_with_answer_input(self) -> None:
        """Test choose calculation conditions with answer input."""
        self.choice_page.test_title()
        self.choice_page.choose_calculation_conditions(
            calculation='add',
            time_answer='1',
            min_value='5',
            max_value='6',
            input_answer_choice=True,
        )
        expect(
            self.page.locator('#question_text')
        ).to_contain_text('5 + 6', timeout=20000)
