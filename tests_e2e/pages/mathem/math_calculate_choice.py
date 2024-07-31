"""
Module for presenting a page for selecting conditions for performing
a mathematical calculation exercise.
"""
import datetime

from playwright.sync_api import Page

from tests_e2e.pages.base import POMPage


class MathCalculateChoicePage(POMPage):
    """Mathematical calculation conditions page class."""

    title = 'Условия задания'
    """Mathematical calculation conditions page title.
    """

    def __init__(self, page: Page, host=None) -> None:
        """Mathematical calculation conditions page constructor."""
        super().__init__(page)
        self.host = host
        self.path = '/task/math-calculate-choice/'
        self.calculation_choice = self.page.get_by_test_id('calculation_type')
        self.time_input = self.page.get_by_label('Время на ответ (сек)*')
        self.min_operand_input = self.page.get_by_label('Минимальное число*')
        self.max_operand_input = self.page.get_by_label('Максимальное число*')
        self.input_answer_choice = self.page.get_by_label('С вводом ответа')
        self.submit_button = self.page.get_by_role('button', name='Начать')

    def choose_calculation_conditions(
        self,
        *,
        calculation: str | None = None,
        time_answer: str | None = None,
        min_value: str | None = None,
        max_value: str | None = None,
        input_answer_choice: bool = False,
    ) -> None:
        """Choose calculation conditions.

        Parameters
        ----------
        calculation : `str` | None
            Choice of mathematical operation, may be: 'mul', 'add', 'sub'.
        time_answer: `str` | None
            Task display time.
        min_value: `str` | None
            Minimum value of the operand.
        max_value: `str` | None
            Maximum value of the operand.
        input_answer_choice: `bool`
            Executing a task with entering an answer if `True`
            otherwise only show the question then answer.
        """
        if calculation:
            assert calculation in ('mul', 'add', 'sub')
            self.calculation_choice.select_option(calculation)
        if time_answer:
            self.time_input.fill(time_answer)
        if min_value:
            self.min_operand_input.fill(min_value)
        if max_value:
            self.max_operand_input.fill(max_value)
        if input_answer_choice:
            self.input_answer_choice.click()
        self.page.screenshot(path=f'screenshot_{datetime.datetime.now()}.png')
        self.submit_button.click()
