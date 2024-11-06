"""Mathematics exercise params, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class MathExerciseParamsPage(POMPage):
    """Mathematics exercise params, the test representation of page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Условия задания'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.page = page
