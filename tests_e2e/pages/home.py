"""The home page representation module."""

from playwright.sync_api import Page

from tests_e2e.pages.base import POMPage


class HomePage(POMPage):
    """The home page representation class.

    Parameters
    ----------
    page : `Page`
        Playwright page instance.

    """

    title = 'Домашняя страница'
    """The Home page title (`str`).
    """

    def __init__(self, page: Page, host: str | None = None) -> None:
        """Home page constructor."""
        super().__init__(page)
        self.path = ''
        self.host = host
