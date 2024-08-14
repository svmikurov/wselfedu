"""Mathematical calculation exercise with answer input page."""

from time import sleep

from playwright.sync_api import Page

from tests_e2e.pages.base import POMPage


class MathCalculateSolutionPage(POMPage):
    """Mathematical calculation solution page class."""

    title = 'Вычисления с вводом ответа'
    """Page title (`str`).
    """

    def __init__(self, page: Page, host: str | None = None) -> None:
        """Mathematical calculation solution page constructor."""
        super().__init__(page)
        self.path = '/task/math-calculate-solution'
        self.page = page
        self.host = host
        self.question_text = page.locator('#question_text')
        self.answer_input = page.locator('#id_user_solution')
        self.submit_btn = page.get_by_role('button', name='Ответить')
        self.back_btn = page.get_by_test_id('btn-back')
        self.evaluation_msg = page.locator('#evaluation_msg')

    def do_the_exercise(self) -> None:
        """Do the exercise."""
        self.question_text.wait_for(state='visible')

        sleep(2)  # Time to complete the task
        question_text = self.question_text.inner_text()

        # first_operand, _, second_operand = question_text.split()
        # task_solution = int(first_operand) * second_operand)
        task_solution = self.page.evaluate(question_text)

        self.answer_input.fill(str(task_solution))
        self.submit_btn.click()
