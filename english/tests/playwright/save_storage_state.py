"""
This module create the signed-in state for the playwright tests
and saves it to file.

Reusing signed in state.
https://playwright.dev/python/docs/auth#reusing-signed-in-state

Run for get signed-in state:
    # add to .env DEFAULT_DB=fixtures
    $ make start                  # need the server running
    $ pytest english/tests/playwright/save_storage_state.py
    # remove from .env DEFAULT_DB=fixtures

Reuse the signed-in state:
    ...
    context = browser.new_context(storage_state="state.json")
"""
from playwright.sync_api import expect, sync_playwright

AUTH_URL = 'http://127.0.0.1:8000/users/login/'
USER_NAME = 'user02'
PASSWORD = '1q2s3d4r'
STATE_PATH = 'english/tests/playwright/.auth/state.json'


with sync_playwright() as playwright:
    browser = playwright.firefox.launch()
    context = browser.new_context()
    page = context.new_page()

    page.goto(AUTH_URL)
    expect(page.get_by_text('Имя пользователя')).to_be_visible()

    # fill form
    page.get_by_placeholder('Имя пользователя').fill(USER_NAME)
    page.get_by_placeholder('Пароль').fill(PASSWORD)
    page.get_by_role('button', name='Войти').click()

    # save storage state
    storage = context.storage_state(path=STATE_PATH)

    expect(page.get_by_text('Домашняя страница')).to_be_visible()
    context.close()
    browser.close()
