import os
from urllib.parse import urljoin

import pytest
from django.core.management import call_command
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

from config import settings

load_dotenv()

TEST_DB_NAME = 'db-wse-pytest.sqlite3'
"""Date base name used by pytest.
"""
FIXTURE_PATH = 'english/tests/fixtures/wse-fixtures-2.json'
COOKIES_PATH = 'english/tests/playwright/.auth/cookies.json'
STATE_PATH = 'english/tests/playwright/.auth/user02_state.json'
BASE_URL = '127.0.0.1:8000'
AUTH_PATH = 'users/login/'

TEST_USER_NAME = os.getenv('TEST_USER_NAME')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')


# https://pytest-django.readthedocs.io/en/latest/database.html#django-db-modify-db-settings
def django_db_modify_db_settings():
    """Run tests with db-wse-pytest.sqlite3 date base.

    Allows to avoid overwriting the date base used in development.
    """
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(settings.BASE_DIR, TEST_DB_NAME)
    }


# https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-test-database-if-you-don-t-use-transactional-or-live-server
# https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-test-database-if-you-use-transactional-or-live-server
@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    """Populate the test database from fixtures."""
    with django_db_blocker.unblock():
        call_command('loaddata', FIXTURE_PATH)


@pytest.fixture(scope='function')
def auth_home_page(page: Page, live_server):
    page.goto(urljoin(live_server.url, AUTH_PATH))
    # fill form
    page.get_by_placeholder('Имя пользователя').fill(TEST_USER_NAME)
    page.get_by_placeholder('Пароль').fill(TEST_PASSWORD)
    page.get_by_role('button', name='Войти').click()
    expect(page.get_by_text('Домашняя страница')).to_be_visible()
    return page


@pytest.mark.browser_context_args(storage_state=STATE_PATH)
def test_state(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_role('link', name='ВыЙтИ')).to_be_visible()
