```cfgrlanguage
HOME_PATH = '/'

def test_home_page_status_api(playwright: Playwright, live_server):
    """Test by API request home page OK status for anonymous."""
    browser: Browser = playwright.chromium.launch()
    context: BrowserContext = browser.new_context(base_url=live_server.url)
    api_request_context: APIRequestContext = context.request

    response: APIResponse = api_request_context.get(HOME_PATH)
    assert response.ok
```

```cfgrlanguage
LOGIN_PATH = 'users/login/'

def test_auth_page_status(test_page):
    url = urljoin(test_page.url, LOGIN_PATH)
    response = test_page.goto(url)
    assert response.ok
    expect(test_page).to_have_title('Вход в приложение')
```