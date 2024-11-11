"""Profile page module."""

from time import sleep

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class ProfilePage(POMPage):
    """Profile page class.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Личный кабинет'
    """Page title (`str`).
    """

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
        self.mult_table_btn = self.page.get_by_role(
            'button', name='Таблица умножения'
        )

    def start_study_mult_table(self) -> None:
        """Start study the multiplication table."""
        self.mult_table_btn.click()
        # Waiting for a request from Ajax
        sleep(2)
