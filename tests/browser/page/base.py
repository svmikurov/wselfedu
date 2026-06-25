"""Base Playwright POM page."""

from __future__ import annotations

from http import HTTPStatus
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
        """Open page and return success response."""
        response = self._page.goto(self.path)
        self._check_status_ok(response)
        return response

    @staticmethod
    def _check_status_ok(response: Response | None) -> None:
        # TODO: Update with human readable handling for assertion error
        assert response
        assert response.status == HTTPStatus.OK
