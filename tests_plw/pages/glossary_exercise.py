"""Term exercise, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class GlossaryExercisePage(POMPage):
    """Term exercise, the test representation of page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Выбор терминов для изучения'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
