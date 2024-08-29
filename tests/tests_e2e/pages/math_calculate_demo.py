"""Mathematical demo calculation exercise page."""

from playwright.sync_api import Page

from tests.tests_e2e.pages.base import POMPage


class MathCalculateDemoPage(POMPage):
    """Mathematical calculation demo page class."""

    title = ''

    def __init__(self, page: Page) -> None:
        """Mathematical calculation demo page constructor."""
        super().__init__(page)
        self.path = 'task/math-calculate-demo'
        self.page = page
        self.question_text = page.locator('#question_text')
        self.answer_text = page.locator('#answer_text')
        self.next_button = page.get_by_role('button', name='Далее')
        self.back_button = page.get_by_test_id('btn-back')
