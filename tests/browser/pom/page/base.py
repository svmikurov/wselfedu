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

    def open(self) -> Response | None:
        """Open page and return response."""
        response = self._page.goto(self.path)
        return response
