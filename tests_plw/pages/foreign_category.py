"""Foreign word category, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ForeignCategoryPage(POMPage):
    """Foreign word category, the test representation of page."""

    title = 'Категории слов'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.page = page