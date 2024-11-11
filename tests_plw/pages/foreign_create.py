"""Foreign word create, the representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ForeignCreatePage(POMPage):
    """Foreign word create, the representation of page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Добавить слово'

    def __init__(self, page: Page) -> None:
        """Construct the sidebar representation."""
        super().__init__(page)
