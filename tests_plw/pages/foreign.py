"""Representation of foreign main page for browser testing."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ForeignMainPage(POMPage):
    """Foreign main page representation.

    :param Page page: Playwright Pytest page fixture.
    """

    title = 'Иностранный язык'

    def __init__(self, page: Page) -> None:
        """Construct the sidebar representation."""
        super().__init__(page)
