"""The user pages representation test module."""

import os

from dotenv import load_dotenv
from playwright.sync_api import expect

from tests_e2e.pages.user import (
    CreateUserPage,
    DeleteUserPage,
    LoginPage,
    authorize_the_page,
)
from tests_e2e.tests.base import POMTest
from tests_plw.pages.home import HomePage
from users.models import UserApp

load_dotenv('./.env_vars/.env.wse')

CREATE_USER_NAME = 'Playwright'
"""Temporary username (`str`).
"""
CREATE_USER_PASS = '1q2s3d4r'
"""Temporary username password (`str`).
"""
USER_NAME = os.getenv('TEST_USER_NAME')
"""Username, typically used by default in tests and fixtures (`str`).
"""
USER_PASS = os.getenv('TEST_USER_PASS')
"""User password, typically used by default in tests and fixtures
(`str`).
"""


class TestCreateUserPage(POMTest):
    """Create user page test class."""

    def test_create_user_page(self) -> None:
        """Test create user page."""
        create_user_page = CreateUserPage(self.page)
        url = f'{self.live_server_url}{create_user_page.path}'
        create_user_page.navigate(url=url)
        create_user_page.test_title()
        create_user_page.create_user(CREATE_USER_NAME, CREATE_USER_PASS)

        # redirect to login page after successful registration
        expect(create_user_page.page).to_have_title(LoginPage.title)

        assert UserApp.objects.filter(username=CREATE_USER_NAME).exists()


class TestLoginPage(POMTest):
    """Login page test."""

    fixtures = ['tests_e2e/fixtures/fixture-db-user.json']

    def test_login_page(self) -> None:
        """Test login page."""
        login_page = LoginPage(self.page)
        login_page.navigate(url=f'{self.live_server_url}{login_page.path}')
        login_page.test_title()
        login_page.login(USER_NAME, USER_PASS)

        # redirect to home page after successful login
        expect(login_page.page).to_have_title(HomePage.title)


class TestDeleteUserPage(POMTest):
    """Test delete user page class."""

    fixtures = ['tests_e2e/fixtures/fixture-db-user.json']

    def test_delete_user_page(self) -> None:
        """Test delete user page."""
        authorize_the_page(self.page, self.live_server_url)

        delete_page = DeleteUserPage(self.page)
        page_path = delete_page.account_link.get_attribute('href')
        delete_page.navigate(url=f'{self.live_server_url}{page_path}')
        delete_page.delete_user()

        # redirect to login page after successful registration
        expect(delete_page.page).to_have_title(LoginPage.title)
        assert not UserApp.objects.filter(username=USER_NAME).exists()
