"""
Test home page not logged in site visitor and logged-in user.

Run
---
    $ pytest -v english/tests/playwright
"""
from playwright.sync_api import Page, expect

from english.tests.playwright.pw_framework import is_role_visible


def test_get_page_status(page: Page, live_server):
    """Test home page status 200."""
    response = page.request.get(live_server.url)
    expect(response).to_be_ok()


def test_home_page_navbar(page: Page, live_server):
    """Test basic navbar."""
    page.goto(live_server.url)

    is_role_visible(page, 'link', 'WSE')
    expect(page.get_by_role('link', name='Английский язык')).to_be_visible()
    expect(page.get_by_role('link', name='Регистрация')).to_be_visible()
    expect(page.get_by_role('link', name='Войти')).to_be_visible()


def test_nome_page_body(page: Page, live_server):
    """Test Упражнение Изучаем слова button."""
    page.goto(live_server.url)

    expect(page.get_by_text('Домашняя страница')).to_be_visible()
    is_role_visible(page, 'button', 'Упражнение "Изучаем слова"')
    is_role_visible(page, 'button', 'Добавить слово в словарь')

    page.get_by_role('button', name='Изучаем слова').click()
    expect(page.get_by_text('Изучаем слова')).to_be_visible()
