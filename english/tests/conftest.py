import os
from urllib.parse import urljoin

import pytest
from django.core.management import call_command
from dotenv import load_dotenv
from playwright.sync_api import (
    Page, expect, sync_playwright, APIRequestContext, BrowserContext
)

from config import settings

load_dotenv()

TEST_DB_NAME = 'db-wse-pytest.sqlite3'
"""Date base name used by pytest.
"""
FIXTURE_PATH = 'english/tests/fixtures/wse-fixtures-4.json'
COOKIES_PATH = 'english/tests/playwright/.auth/cookies.json'
STATE_PATH = 'english/tests/playwright/.auth/user02_state.json'
AUTH_PATH = 'users/login/'

TEST_USER_NAME = os.getenv('TEST_USER_NAME')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')


# https://pytest-django.readthedocs.io/en/latest/database.html#django-db-modify-db-settings
def django_db_modify_db_settings() -> None:
    """Run tests with TEST_DB_NAME date base.

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
    """Load the Django fixture FIXTURE_PATH.

    Override django_db_setup fixture.

    Mark tests with the @pytest.mark.django_db().
    """
    with django_db_blocker.unblock():
        call_command('loaddata', FIXTURE_PATH)


@pytest.fixture(scope='function')
def auth_home_page(page: Page, live_server) -> Page:
    """Return page with logged-in user."""
    page.goto(urljoin(live_server.url, AUTH_PATH))
    # fill form
    page.get_by_placeholder('Имя пользователя').fill(TEST_USER_NAME)
    page.get_by_placeholder('Пароль').fill(TEST_PASSWORD)
    page.get_by_role('button', name='Войти').click()
    expect(page.get_by_text('Домашняя страница')).to_be_visible()
    return page


@pytest.fixture(scope='function')
def auth_context(auth_home_page) -> BrowserContext:
    """Return page context with logged-in user."""
    return auth_home_page.context


@pytest.fixture(scope='function')
def test_page(page: Page, live_server) -> Page:
    """Return page with started server."""
    page.goto(live_server.url)
    return page


@pytest.fixture()
def api_request_context(live_server) -> APIRequestContext:
    """Create a new request context.

    https://earthly.dev/blog/playwright-python-api-testing/
    Returns:
        APIRequestContext
    """
    with sync_playwright() as playwright:
        api_request_context: APIRequestContext = playwright.request.new_context(
            base_url=live_server.url
        )
        yield api_request_context
        api_request_context.dispose()


@pytest.fixture(scope='function')
def browser_context_args(browser_context_args):
    """Set browser context args.

    https://pypi.org/project/pytest-playwright/0.1.1/
    """
    return {
        **browser_context_args,
        "viewport": {
            # Allows you to avoid covering the playwright tests screen with the
            # toolbar panel.
            # size WSXGA+ / 1680 × 1050 / 16:10
            "width": 1680,
            "height": 1050,
        }
    }
