from playwright.sync_api import Page

from tests_e2e.pages.base import TestPage


class HomePage(TestPage):
    """The home page representation class."""

    title = 'Домашняя страница'

    def __init__(self, page: Page):
        super().__init__(page)
        self.path = ''
