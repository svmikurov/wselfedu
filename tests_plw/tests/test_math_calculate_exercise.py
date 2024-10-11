"""E2E test table multiplication exercise page module.

Testing using the :obj:`MathCalculateExersicePage
<tests_plw.pages.math_calculate_exercise.MathCalculateExersicePage>`
page representation class.
"""

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
        self.authorize_test_page()
        # To set task conditions for bonus exercise need go to
        # '/math/math-set-table-mult-points/'
        self.page_path = '/math/math-set-table-mult-points/'
        self.test_page.navigate(page_url=self.page_url)

    def test_title(self) -> None:
        """Test table mult exercise title."""
        self.test_page.test_title()

    def test_do_the_exercise(self) -> None:
        """Test do the exercise."""
        self.test_page.do_the_exercise()
        expect(self.test_page.evaluation_msg).to_have_text('Верно!')
