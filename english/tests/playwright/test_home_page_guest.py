"""
Test actions and views for anonymous.
"""
from urllib.parse import urljoin

from playwright.sync_api import Page, expect


def test_home_page_status(page: Page, live_server):
    """Test home page status for anonymous."""
    response = page.request.get(live_server.url)
    expect(response).to_be_ok()
    assert response.ok


def test_home_page_title(test_page: Page):
    """Test home page content for anonymous."""
    expect(test_page).to_have_title('WSE: Домашняя страница')


def test_home_page_navbar(page: Page, live_server):
    """Test home page content for anonymous."""
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


def test_home_page_content(test_page: Page):
    """Test home page content for anonymous."""
    home_url = test_page.url

    test_page.get_by_role('button', name='Упражнение \"Изучаем слова\"').click()
    expect(test_page).to_have_title('Изучаем слова')

    test_page.goto(home_url)
    test_page.get_by_role('button', name='Добавить слово в словарь').click()
    expect(test_page).to_have_title('Добавить слово')
