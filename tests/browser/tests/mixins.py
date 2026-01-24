"""Browser POM test mixins."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING, Generic, TypeVar

from playwright.sync_api import Page, expect

from ..pages.base import BasePage

if TYPE_CHECKING:
    from playwright.sync_api import Response

T = TypeVar('T', bound=BasePage)


class OpenPageMixin(Generic[T]):
    """Provides open page browser POM test.

    Test via mixin:
        - status code is OK
        - page have correct title
    """

    response: Response
    page: T
    _page: Page

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
