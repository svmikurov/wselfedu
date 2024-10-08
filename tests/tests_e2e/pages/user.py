"""The user pages representation module."""

import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

from tests.tests_e2e.pages.base import POMPage
from tests_plw.pages.home import HomePage

load_dotenv('./.env_vars/.env.wse')

USER_NAME = os.getenv('TEST_USER_NAME')
"""Username, typically used by default in tests and fixtures.
"""
USER_PASS = os.getenv('TEST_USER_PASS')
"""User password, typically used by default in tests and fixtures.
"""


class CreateUserPage(POMPage):
    """Class representing the user registration page.

    Parameters
    ----------
    page : `Page`
        Playwright page.

    Arguments
    ---------
    path : `str`
        Page path.
    user_name_input : `Locator`
        Username field input locator.
    password1_input : `Locator`
        Password field input locator.
    password2_input : `Locator`
        Confirm password field input locator.
    submit_button : `Locator`
        Submit button locator.

    """

    title = 'Регистрация пользователя'
    """Create page title.
    """

    def __init__(self, page: Page) -> None:
        """Create page constructor."""
        super().__init__(page)
        self.path = '/users/registration/'
        self.user_name_input = page.get_by_placeholder('Имя пользователя')
        self.password1_input = page.get_by_placeholder('Пароль')
        self.password2_input = page.get_by_placeholder('Подтверждение пароля')
        self.submit_button = page.get_by_role(
            'button',
            name='Зарегистрироваться',
        )

    def create_user(self, user_name: str, user_pass: str) -> None:
        """Register a new user.

        Fills out the user registration form. Clicks on the submit form
        button.

        Parameters
        ----------
        user_name : `str`
            Login of the registered user.
        user_pass : `str`
            Password of the registered user.

        """
        self.user_name_input.fill(user_name)
        self.password1_input.fill(user_pass)
        self.password2_input.fill(user_pass)
        self.submit_button.click()


class LoginPage(POMPage):
    """Class representing the login page."""

    title = 'Вход в приложение'
    """Page title.
    """

    def __init__(self, page: Page) -> None:
        """Login page constructor."""
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


class DeleteUserPage(POMPage):
    """Class representing the delete user page."""

    title = 'Удаление пользователя'
    """Page title.
    """

    def __init__(self, page: Page) -> None:
        """User delete page constructor."""
        super().__init__(page)
        self.account_link = page.get_by_test_id('account-link')
        self.delete_button = page.get_by_role('link', name='Удалить')
        self.confirm_button = page.get_by_role('button', name='Удалить')

    def delete_user(self) -> None:
        """Delete user."""
        self.delete_button.click()
        self.confirm_button.click()


def authorize_the_page(
    page: Page,
    host: str,
    user_name: str | None = None,
    user_pass: str | None = None,
) -> None:
    """Authorize the page.

    Authorizes the user on the login page by filling out the login
    form. If no user is specified, authorizes the default user,
    typically used by default in tests and fixtures.

    Parameters
    ----------
    page : `Page`
        Playwright page for authorize.
    host : `str`
        Host or Django ``live_server_url``.
    user_name : `str` | None
        The username (username commonly used in tests and fixtures, by
        default)
    user_pass : `str` | None
        The user password (username password commonly used in tests and
        fixtures, by default)

    """
    login_page = LoginPage(page)
    user = user_name or USER_NAME
    password = user_pass or USER_PASS

    login_page.navigate(url=f'{host}{login_page.path}')
    login_page.login(user, password)

    # after successful authentication the user is redirected to the
    # home page
    expect(login_page.page).to_have_title(HomePage.title)
