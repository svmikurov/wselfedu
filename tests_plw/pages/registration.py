"""Registration, the test representation of page."""

from playwright.sync_api import Page

from tests_plw.pages.base import POMPage


class RegistrationPage(POMPage):
    """Registration, the test representation of page.

    :param Page page: The Playwright Pytest page fixture.
    """

    title = 'Регистрация пользователя'

    def __init__(self, page: Page) -> None:
        """Construct the page."""
        super().__init__(page)
