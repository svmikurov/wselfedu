from playwright.sync_api import Page, expect

HOME_URL = 'http://127.0.0.1:8000/'
"""Home page URL.
"""


def test_home(page: Page):
    """Тест кнопки перехода на упражнение Изучаем слова."""
    page.goto(HOME_URL)
    page.get_by_role('button', name='Изучаем слова').click()
    expect(page.get_by_text('Изучаем слова')).to_be_visible()


def test_nome_not_auth_user(page: Page):
    pass
