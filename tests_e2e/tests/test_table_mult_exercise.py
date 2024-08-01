from django.core.cache import cache
from playwright.sync_api import expect

from tests_e2e.pages.math_calculate_solution import MathCalculateSolutionPage
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import POMBaseTest


class TestTableMultExercise(POMBaseTest):
    """Test table multiplication exercise page class."""

    fixtures = ['tests_e2e/fixtures/fixture-db-exercise-word-study']
    user_id = 1

    def setUp(self) -> None:
        """Choice words according to the user's exercise conditions.

        Authorizes the page before.
        """
        super().setUp()
        self.host = str(self.live_server_url)

        authorize_the_page(self.page, self.host)

        self.test_page = MathCalculateSolutionPage(self.page)
        self.test_page.navigate(host=self.host)

        # To set task conditions for bonus exercise need go to
        # '/task/math-set-table-mult-points/'
        url_set_conditions = f'{self.host}/task/math-set-table-mult-points/'
        self.test_page.navigate(url=url_set_conditions)

    def test_title(self) -> None:
        """Test table mult exercise title."""
        self.test_page.test_title()

    def test_cache_time_start_exercise(self) -> None:
        """Test note in cache time start exercise."""
        self.test_page.question_text.wait_for(state='visible')
        key_name = 'user_1_exc_mul_start_time'
        assert cache.get(key_name)

    def test_do_the_exercise(self) -> None:
        """Test do the exercise."""
        self.test_page.do_the_exercise()
        expect(self.test_page.evaluation_msg).to_have_text('Верно!')
