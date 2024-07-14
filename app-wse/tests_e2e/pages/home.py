from playwright.sync_api import Page


class HomePage:
    """The home page representation class."""

    title = 'Домашняя страница'

    def __init__(self, page: Page):
        self.page = page
        self.path = ''

    def navigate(self, host):
        """Navigate to page."""
        self.page.goto(host + self.path)
