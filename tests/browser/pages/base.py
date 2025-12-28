"""Base Playwright POM page."""

from __future__ import annotations

from typing import TYPE_CHECKING

from playwright.sync_api import Page

if TYPE_CHECKING:
    from playwright.sync_api import Response


class BasePage:
    """Base Playwright POM page."""

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

    def open(self) -> Response | None:
        """Open page and return response."""
        response = self._page.goto(self.path)
        return response
