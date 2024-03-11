import os
from urllib.parse import urljoin

import pytest
from playwright.sync_api import expect

REGISTRATION_PATH = 'users/registration/'
LOGIN_PATH = 'users/login/'

TEST_USER_NAME = os.getenv('TEST_USER_NAME')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')


@pytest.mark.skip
def test_user_registration():
    ...


@pytest.mark.django_db()
def test_user_authentication_page(test_page):
    """Test user authentication page."""
    base_url = test_page.url
    response = test_page.goto(urljoin(base_url, LOGIN_PATH))

    expect(test_page).to_have_title('Вход в приложение')

    test_page.get_by_placeholder('Имя пользователя').fill(TEST_USER_NAME)
    test_page.get_by_placeholder('Пароль').fill(TEST_PASSWORD)
    test_page.get_by_role('button', name='Войти').click()

    expect(test_page).to_have_title('WSE: Домашняя страница')
