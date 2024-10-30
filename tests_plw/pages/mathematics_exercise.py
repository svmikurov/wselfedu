"""Mathematics exercise, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class MathExercisePage(POMPage):
    """Mathematics exercise, the test representation of page."""

    title = 'Условия задания'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.page = page
