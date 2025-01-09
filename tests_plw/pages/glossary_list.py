"""Term term list, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class TermListPage(POMPage):
    """Term term list, the test representation of page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Термины глоссария'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
