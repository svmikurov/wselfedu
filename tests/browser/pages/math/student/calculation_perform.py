"""Student's calculation exercise performing page."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.utils.translation import gettext as _

from tests.browser.pages import base

if TYPE_CHECKING:
    from playwright.sync_api import Page


class StudentCalculationPerformPage(
    base.BasePage,
):
    """Student's calculation exercise performing page."""

    def __init__(self, page: Page, path: str) -> None:
        """Construct the page."""
        super().__init__(page)

        self.title = _('math.page.calculation.index.title')
        self.path = path
