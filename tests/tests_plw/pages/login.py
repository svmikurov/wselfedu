"""Login page representation module."""

from playwright.async_api import Page

from tests.tests_plw.pages.base import POMPage


class LoginPage(POMPage):
    """Class representing the login page."""

    title = 'Вход в приложение'
    """Page title (`str`).
    """

    def __init__(self, page: Page) -> None:
        """Construct the login page."""
        super().__init__(page)
        self.path = '/users/login'
        self.username_input = page.get_by_placeholder('Имя пользователя')
        self.password_input = page.get_by_placeholder('Пароль')
        self.submit_button = page.get_by_test_id('login-button')

    def login(self, username: str, password: str) -> None:
        """Login.

        Fills out the user login form. Clicks on the submit form button.

        Parameters
        ----------
        username : `str`
            Username for login.
        password : `str`
            Password for login.

        """
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.submit_button.click()
