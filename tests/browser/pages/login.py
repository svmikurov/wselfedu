"""Defines Login page gor POM browser testing."""

from tests.browser.pages.base import BasePage


class LoginPage(BasePage):
    """Login page."""

    title = 'Login'
    path = 'login/'

    def _set_locators(self) -> None:
        self.username = self._page.locator('input#id_username')
        self.password = self._page.locator('input#id_password')
        self.submit = self._page.get_by_role('button', name='Подтвердить')

    def login(self, username: str, password: str) -> None:
        """Login."""
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()
