"""
Test home page for anonymous.
"""
from urllib.parse import urljoin

import pytest
from playwright.sync_api import Page, expect, Response


@pytest.fixture
def go_to_home(page: Page, live_server):
    host = live_server.url
    url = urljoin(host, '/')
    return page.goto(url)


def test_home_page_status(go_to_home: Response):
    """Test home page status for anonymous."""
    assert go_to_home.ok


def test_home_page_title(page: Page, go_to_home: Page):
    """Test home page title for anonymous."""
    expect(page).to_have_title('WSE: Домашняя страница')


def test_home_page_navbar(page: Page, live_server):
    """Test navbar for anonymous."""
    host = live_server.url
    locators = (
        ('WSE', '/'),
        ('Английский язык', 'english/'),
        ('Войти', 'users/login/'),
        ('Регистрация', 'users/registration/'),
    )

    for loc in locators:
        page.goto(host)
        page.get_by_role('link', name=loc[0]).click()
        expect(page).to_have_url(urljoin(host, loc[1]))


def test_home_page_content(go_to_home: Page, page: Page):
    """Test home page content for anonymous."""
    url = go_to_home.url

    page.get_by_role('button', name='Упражнение \"Изучаем слова\"').click()
    expect(page).to_have_title('Изучаем слова')

    page.goto(url)
    page.get_by_role('button', name='Добавить слово в словарь').click()
    expect(page).to_have_title('Добавить слово')
