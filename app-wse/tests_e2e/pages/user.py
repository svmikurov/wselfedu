"""
User pages module.
"""
import os

from dotenv import load_dotenv
from playwright.sync_api import Page, expect

from tests_e2e.pages.base import TestPage
from tests_e2e.pages.home import HomePage

load_dotenv()

USER_NAME = os.getenv('TEST_USER_NAME')
USER_PASS = os.getenv('TEST_USER_PASS')


class CreateUserPage(TestPage):
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
    """ Page title.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.path = '/users/registration/'
        self.user_name_input = page.get_by_placeholder('Имя пользователя')
        self.password1_input = page.get_by_placeholder('Пароль')
        self.password2_input = page.get_by_placeholder('Подтверждение пароля')
        self.submit_button = page.get_by_role(
            'button', name='Зарегистрироваться',
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


class LoginPage(TestPage):
    """Class representing the login page."""

    title = 'Вход в приложение'

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.path = '/users/login'
        self.username_input = page.get_by_placeholder("Имя пользователя")
        self.password_input = page.get_by_placeholder("Пароль")
        self.submit_button = page.get_by_test_id("login-button")

    def login(self, username: str, password: str) -> None:
        """Test login.

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


class DeleteUserPage(TestPage):
    """Class representing the delete user page."""

    title = 'Удаление пользователя'

    def __init__(self, page: Page):
        super().__init__(page)
        self.account_link = page.get_by_test_id("account-link")
        self.delete_button = page.get_by_role("link", name="Удалить")
        self.confirm_button = page.get_by_role("button", name="Удалить")

    def delete_user(self):
        """Delete user."""
        self.delete_button.click()
        self.confirm_button.click()


def authorize_the_page(page: Page, host: str) -> None:
    """Authorize the page.

    Parameters
    __________
    page : `Page`
        Playwright page for authorize.
    host : `str`
        Host or Django ``live_server_url``.
    """
    login_page = LoginPage(page)
    login_page.navigate(f"{host}{login_page.path}")
    login_page.login(USER_NAME, USER_PASS)
    expect(login_page.page).to_have_title(HomePage.title)
