from urllib.parse import urljoin

import pytest
from playwright.sync_api import Page, expect

from english.models import WordsFavoritesModel

pytestmark = pytest.mark.django_db

WORD_LIST_PATH = 'english/word/list/'


def is_favorite_word(user_id, word_id) -> bool:
    """Check if word is favorite word."""
    return WordsFavoritesModel.objects.filter(
        user_id=user_id, word_id=word_id
    ).exists()


@pytest.mark.browser_context_args
def test_add_word_to_favorites_via_list_table(auth_home_page: Page):
    """Test add word to favorites via word list table."""
    user_id = 3
    word_id = 9
    page = auth_home_page
    host = page.url
    url = urljoin(host, WORD_LIST_PATH)
    page.goto(url)

    add_button = page.get_by_role(
        'row', name=f'word_u{user_id}_w{word_id}'
    ).get_by_role('button', name='Добавить')
    remove_button = page.get_by_role(
        'row', name=f'word_u{user_id}_w{word_id}'
    ).get_by_role('button', name='Убрать')

    add_button.click()
    expect(remove_button).to_be_visible()
    assert is_favorite_word(user_id, word_id)
    remove_button.click()
    assert not is_favorite_word(user_id, word_id)
    expect(add_button).to_be_visible()
