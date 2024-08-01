"""
Module for presenting a page this mathematical calculation exercise
with answer input.
"""

from playwright.sync_api import Page

from tests_e2e.pages.base import POMPage


class MathCalculateSolutionPage(POMPage):
    """Mathematical calculation solution page class."""

    title = 'Вычисления с вводом ответа'

    def __init__(self, page: Page) -> None:
        """Mathematical calculation solution page constructor."""
        super().__init__(page)
        self.path = '/task/math-calculate-solution'
        self.page = page
        self.question_text = page.locator('#question_text')
        self.answer_input = page.locator('#id_user_solution')
        self.submit_button = page.get_by_role('button', name='Ответить')
        self.back_button = page.get_by_test_id('btn-back')
