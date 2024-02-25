from urllib.parse import urljoin

from playwright.sync_api import Page, expect

USER_ID = 2


def get_account_path():
    return f'users/{USER_ID}/account/'


def test_account_page_status(page: Page, live_server):
    url = urljoin(live_server.url, get_account_path())
    response = page.request.get(url)
    expect(response).to_be_ok()

    page.goto(url)
