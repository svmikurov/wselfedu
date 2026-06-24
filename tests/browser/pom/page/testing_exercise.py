"""Testing exercise POM page."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .base import BasePage

if TYPE_CHECKING:
    from playwright.sync_api import Page


class TestingExercisePage(BasePage):
    """Testing exercise POM page."""

    __test__ = False

    path = '/testing/'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._set_locators()

    def _set_locators(self) -> None:
        self.question_text = self._page.get_by_test_id('question-text')
