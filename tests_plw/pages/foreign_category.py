"""Foreign word category, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ForeignCategoryPage(POMPage):
    """Foreign word category, the test representation of page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Категории слов'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
