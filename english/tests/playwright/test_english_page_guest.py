from typing import Union
from urllib.parse import urljoin

import pytest
from playwright.sync_api import Page, expect, Response

PAGE_ELEMENTS: list[dict] = [
    {'locator': 'button',
     'name': 'Изучаем слова',
     'path': 'task/english-translate-choice/'},
    {'locator': 'button',
     'name': 'Добавить слово',
     'path': 'english/word/create/'},
    {'locator': 'button',
     'name': 'Список слов',
     'path': 'english/word/list/'},
    {'locator': 'button',
     'name': 'Категории',
     'path': 'english/categories/list/'},
    {'locator': 'button',
     'name': 'Источники',
     'path': 'english/sources/list/'},
]
"""Page content elements designated as locator, name, value for assertion in
 test (`list[dict]`).
"""


@pytest.fixture
def go_to_english(page: Page, live_server) -> Union[Response, None]:
    """Start server and go to 'english/' path page."""
    host = live_server.url
    url = urljoin(host, 'english/')
    return page.goto(url)


def test_english_page_status(go_to_english: Response):
    """Test 'english/' path page status 200."""
    assert go_to_english.ok


def test_english_page_title(page: Page, go_to_english: Response):
    """Test 'english/' path page title."""
    expect(page).to_have_title('Английский язык')


def test_english_page_content(auth_home_page: Page):
    page = auth_home_page
    host = page.url
    url = urljoin(host, 'english/')
    for element in PAGE_ELEMENTS:
        page.goto(url)
        page.get_by_role(element['locator'], name=element['name']).click()
        assert page.url == urljoin(host, element['path'])
