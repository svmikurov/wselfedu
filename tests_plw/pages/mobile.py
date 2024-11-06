"""The representation of page about mobile version application."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class MobilePage(POMPage):
    """The mobile page representation class.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Приложение для мобильных'
    """The Home page title (`str`).
    """

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.path = 'mobile/'
