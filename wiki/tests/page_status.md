```cfgrlanguage
def test_account_page_status(page: Page, live_server):
    url = urljoin(live_server.url, f'users/{USER_ID}/account/')
    response = page.request.get(url)
    expect(response).to_be_ok()
```