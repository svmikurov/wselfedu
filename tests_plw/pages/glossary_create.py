"""Glossary term create, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class TermCreatePage(POMPage):
    """Glossary term create, the test representation of page."""

    title = 'Добавить термин в глоссарий'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.page = page
