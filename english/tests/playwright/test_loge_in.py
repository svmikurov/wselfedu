"""
Test home page not logged in site visitor and logged-in user.

Run
---
    $ pytest -v english/tests/playwright
"""
from urllib.parse import urljoin

import pytest
from playwright.sync_api import Page, expect

AUTH_PATH = 'users/login/'
USER_NAME = 'user02'
PASSWORD = '1q2s3d4r'
STATE_PATH = 'english/tests/playwright/.auth/user0_auth_state.json'


def test_home_page_status(page: Page, live_server):
    """Test home page status 200."""
    response = page.request.get(live_server.url)
    expect(response).to_be_ok()


def test_home_page_anonymous(page: Page, live_server):
    """Test home page for anonymous."""
    page.goto(live_server.url)

    expect(page.get_by_text('Домашняя страница')).to_be_visible()
    expect(page.get_by_role('button', name='Упражнение "Изучаем слова"')).to_be_visible()
    expect(page.get_by_role('button', name='Добавить слово в словарь')).to_be_visible()

    page.get_by_role('button', name='Изучаем слова').click()
    expect(page.get_by_text('Изучаем слова')).to_be_visible()


@pytest.mark.django_db
def test_loge_in_and_home_page(page: Page, live_server):
    """Test home page with loge-in site visitor.

    Test loge-in."""
    # loge-in
    page.goto(urljoin(live_server.url, AUTH_PATH))
    page.get_by_placeholder('Имя пользователя').fill(USER_NAME)
    page.get_by_placeholder('Пароль').fill(PASSWORD)

    page.get_by_role('button', name='Войти').click()
    expect(page.get_by_text('Домашняя страница')).to_be_visible()

    # test home page with loge-in site visitor
    page.goto(live_server.url)
    expect(page.get_by_text('Домашняя страница')).to_be_visible()
    expect(page.get_by_role('link', name='Выйти')).to_be_visible()


def test_home_page_navbar(page: Page, live_server):
    """Test basic navbar."""
    page.goto(live_server.url)

    expect(page.get_by_role('link', name='WSE')).to_be_visible()
    expect(page.get_by_role('link', name='Английский язык')).to_be_visible()
    expect(page.get_by_role('link', name='Регистрация')).to_be_visible()
    expect(page.get_by_role('link', name='Войти')).to_be_visible()
