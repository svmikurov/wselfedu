from task.task_mng import TaskManager
from tests_e2e.pages.math_calculate_solution import MathCalculateSolutionPage
from tests_e2e.pages.user import authorize_the_page
from tests_e2e.tests.base import POMBaseTest

task_mng = TaskManager()


class TestTableMultExercise(POMBaseTest):
    """"""

    fixtures = ['tests_e2e/fixtures/fixture-db-exercise-word-study']

    def setUp(self) -> None:
        """Choice words according to the user's exercise conditions.

        Authorizes the page before.
        """
        self.host = self.live_server_url
        authorize_the_page(self.page, self.host)
        self.test_page = MathCalculateSolutionPage(self.page)
        self.test_page.navigate(host=self.host)

    def test_page(self):
        # To get task conditions for bonus exercise need go to
        # '/task/math-set-table-mult-points/'
        url_set_conditions = '/task/math-set-table-mult-points/'
        self.test_page.navigate(url=f'{self.host}{url_set_conditions}')
        self.test_page.test_title()
