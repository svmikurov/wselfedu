"""Foreign word source, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ForeignSourcePage(POMPage):
    """Foreign word source, the test representation of page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Источники'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.page = page
