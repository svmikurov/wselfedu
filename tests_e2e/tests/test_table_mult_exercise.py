import os
from time import sleep

from django.core.cache import cache

from tests_e2e.pages.math_calculate_solution import MathCalculateSolutionPage
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import POMBaseTest


class TestTableMultExercise(POMBaseTest):
    """"""

    fixtures = ['tests_e2e/fixtures/fixture-db-exercise-word-study']
    user_id = 1
    screenshot_dir = f'tests_e2e/screenshots{os.path.dirname(__file__)}'

    def setUp(self) -> None:
        super().setUp()
        """Choice words according to the user's exercise conditions.

        Authorizes the page before.
        """
        self.host = str(self.live_server_url)
        authorize_the_page(self.page, self.host)

        self.test_page = MathCalculateSolutionPage(self.page)
        self.test_page.navigate(host=self.host)

        # To get task conditions for bonus exercise need go to
        # '/task/math-set-table-mult-points/'
        self.url_set_conditions = (f'{self.host}'
                                   f'/task/math-set-table-mult-points/')
        self.test_page.navigate(url=self.url_set_conditions)

    def test_title(self):
        """Test table mult exercise title."""
        self.test_page.test_title()
        # Need to wait until receive an ajax request
        sleep(2)
        self.page.screenshot(path=self.screenshot_dir + 'test_title.png')

    def test_cache_time_start_exercise(self):
        """Test note in cache time start exercise."""
        self.test_page.navigate(url=self.url_set_conditions)
        key_name = 'user_1_exc_mul_start_time'
        assert cache.get(key_name)
