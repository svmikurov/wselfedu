"""Browser POM test mixins."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from playwright.sync_api import expect

if TYPE_CHECKING:
    from playwright.sync_api import Page, Response

    from ..pages.base import BasePage

    type PageAttributes = BasePage
    type PageState = Page


class OpenPageMixin:
    """Provides open page browser POM test."""

    response: Response
    page: PageAttributes
    _page: PageState

    def test_open_page(self) -> None:
        """Page opens success."""
        # Act
        response = self.page.open()

        # Assert
        # - got response
        assert response is not None, 'The page did not load'

        # - status code is 200
        assert response.status == HTTPStatus.OK, f'Error: {response.status}'

        # - have correct title
        expect(self._page).to_have_title(self.page.title)
