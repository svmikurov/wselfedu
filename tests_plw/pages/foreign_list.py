"""Foreign word list, the representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ForeignListPage(POMPage):
    """Foreign word list, the representation of page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Список слов'

    def __init__(self, page: Page) -> None:
        """Construct the sidebar representation."""
        super().__init__(page)
        self.page = page
