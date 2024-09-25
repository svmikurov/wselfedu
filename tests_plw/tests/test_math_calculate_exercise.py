"""E2E test table multiplication exercise page module.

Testing using the :obj:`MathCalculateExersicePage
<tests_plw.pages.math_calculate_exercise.MathCalculateExersicePage>`
page representation class.
"""

from unittest import skip

from django.core.cache import cache
from playwright.sync_api import expect

from tests_plw.pages.math_calculate_exercise import (
    MathCalculateExercisePage,
)
from tests_plw.tests.base import POMTest


class MathematicalCalculateExerciseTest(POMTest):
    """Test table multiplication exercise page class."""

    def setUp(self) -> None:
        """Choice words according to the user's exercise conditions.

        Authorizes the page before.
        """
        super().setUp()
        self.test_page = MathCalculateExercisePage(self.page)
        self.create_user()
        self.authorize_test_page()
        # To set task conditions for bonus exercise need go to
        # '/task/math-set-table-mult-points/'
        self.page_path = '/task/math-set-table-mult-points/'
        self.test_page.navigate(page_url=self.page_url)

    def test_title(self) -> None:
        """Test table mult exercise title."""
        self.test_page.test_title()

    @skip('Test is not stable.')
    def test_cache_time_start_exercise(self) -> None:
        """Test note in cache time start exercise."""
        self.test_page.question_text.wait_for(state='visible')
        key_name = 'user_1_exc_mul_start_time'
        assert cache.get(key_name)

    def test_do_the_exercise(self) -> None:
        """Test do the exercise."""
        self.test_page.do_the_exercise()
        expect(self.test_page.evaluation_msg).to_have_text('Верно!')
