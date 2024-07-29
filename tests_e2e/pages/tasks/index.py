"""
The all tasks page representation module.
"""
from playwright.sync_api import Page

from tests_e2e.pages.base import POMPage


class IndexTaskPage(POMPage):
    """The all tasks page representation class."""

    title = 'Все упражнения'
    """The all tasks index page title (`str`).
    """

    def __init__(self, page: Page, host: str | None = None) -> None:
        """Page constructor."""
        super().__init__(page)
        self.path = '/task/index'
        self.page = page
        self.host = host
        self.mult_table_btn = page.get_by_role(
            'button',
            name='Таблица умножения',
        )
