"""The home page representation module."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class HomePage(POMPage):
    """The home page representation class.

    :param Page page: Playwright Pytest page fixture.
    """

    title = 'WSE Главная'
    """The Home page title (`str`).
    """

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.path = '/'
