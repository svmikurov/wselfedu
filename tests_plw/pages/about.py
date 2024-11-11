"""The about project page representation module."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class AboutPage(POMPage):
    """The about page representation class.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'О проекте'
    """The Home page title (`str`).
    """

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.path = 'about/'
