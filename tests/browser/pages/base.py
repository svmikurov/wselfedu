"""Defines base page for browser POM testing."""

from playwright.sync_api import Page


class BasePage:
    """Base page for POM browser testing."""

    title: str
    path: str

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        self._page = page
        self._set_locators()

    def _set_locators(self) -> None:
        """Set page locators.

        For example:

            def _set_locators(self) -> None:
                self.username = self._page.locator('input#id_username')
                self.password = self._page.locator('input#id_password')
                self.submit = self._page.get_by_role('button')

        """
        pass

    def open(self) -> None:
        """Open current page."""
        self._page.goto(self.path)
