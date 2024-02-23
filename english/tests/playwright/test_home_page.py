"""
Test home page not logged in site visitor and logged-in user.
"""

from playwright.sync_api import Page, expect

from english.tests.playwright.pw_framework import is_role_visible

HOME_URL = 'http://127.0.0.1:8000/'
"""Home page URL.
"""


def get_page_status(page: Page):
    """Test home page status 200."""
    response = page.request.get(HOME_URL)
    expect(response).to_be_ok()


def test_home_page_navbar(page: Page):
    """Test basic navbar."""
    page.goto(HOME_URL)

    is_role_visible(page, 'link', 'WSE')
    expect(page.get_by_role('link', name='Английский язык')).to_be_visible()
    expect(page.get_by_role('link', name='Регистрация')).to_be_visible()
    expect(page.get_by_role('link', name='Войти')).to_be_visible()


def test_nome_page_body(page: Page):
    """Тест кнопки перехода на упражнение Изучаем слова."""
    page.goto(HOME_URL)

    expect(page.get_by_text('Домашняя страница')).to_be_visible()
    is_role_visible(page, 'button', 'Упражнение "Изучаем слова"')
    is_role_visible(page, 'button', 'Добавить слово в словарь')

    page.get_by_role('button', name='Изучаем слова').click()
    expect(page.get_by_text('Изучаем слова')).to_be_visible()


def test_nome_page_auth_user(page: Page):
    pass
