"""Representation of foreign index page for browser testing."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ForeignPage(POMPage):
    """Foreign index page representation.

    :param Page page: Playwright Pytest page fixture.
    """

    title = 'Иностранный язык'

    def __init__(self, page: Page) -> None:
        """Construct the sidebar representation."""
        super().__init__(page)
        self.page = page
