```cfgrlanguage
"""
This module create the signed-in state for the playwright tests
and saves it to file.

Reusing signed in state.
https://playwright.dev/python/docs/auth#reusing-signed-in-state

Run for get signed-in state:
    $ pytest english/tests/playwright/test_storage_state.py --liveserver 127.0.0.1:8000
[page_status.md](page_status.md)
Reuse the signed-in state:
    ...
    context = browser.new_context(storage_state="state.json")
or use:
    @pytest.mark.browser_context_args(storage_state="state.json")
"""
from urllib.parse import urljoin

import pytest
from playwright.sync_api import expect, sync_playwright, BrowserContext, Page

AUTH_PATH = 'users/login/'
USER_NAME = 'user02'
PASSWORD = '1q2s3d4r'
STATE_PATH = 'english/tests/playwright/.auth/user02_state.json'


@pytest.mark.storage
def test_storage_state(context: BrowserContext, live_server) -> None:
    """Set and save storage state."""
    page: Page = context.new_page()
    page.goto(urljoin(live_server.url, AUTH_PATH))
    # fill form
    page.get_by_placeholder('Имя пользователя').fill(USER_NAME)
    page.get_by_placeholder('Пароль').fill(PASSWORD)
    page.get_by_role('button', name='Войти').click()
    # save storage state
    context.storage_state(path=STATE_PATH)
    expect(page.get_by_text('Домашняя страница')).to_be_visible()
    context.close()

```