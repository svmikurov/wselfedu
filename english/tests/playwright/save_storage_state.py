"""
This module create the signed-in state for the playwright tests
and saves it to file.

Reusing signed in state.
https://playwright.dev/python/docs/auth#reusing-signed-in-state

Run:
    pytest english/tests/playwright/save_storage_state.py

Reuse:
    context = browser.new_context(storage_state="state.json")
"""

from playwright.sync_api import sync_playwright

AUTH_URL = 'http://127.0.0.1:8000/users/login/'
USER_NAME = 'user02'
PASSWORD = '1q2s3d4r'
SAVE_STATE_PATH = 'english/tests/playwright/.auth/user02_auth_state.json'


with sync_playwright() as playwright:
    browser = playwright.firefox.launch()
    context = browser.new_context()
    page = context.new_page()

    page.goto(AUTH_URL)

    page.get_by_placeholder('Имя пользователя').fill(USER_NAME)
    page.get_by_placeholder('Пароль').fill(PASSWORD)
    page.get_by_role('button', name='Войти').click()

    storage = context.storage_state(path=SAVE_STATE_PATH)

    context.close()
    browser.close()
