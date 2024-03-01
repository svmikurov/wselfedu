import os
from urllib.parse import urljoin

import pytest
from playwright.sync_api import BrowserContext, APIRequestContext, Page

REGISTRATION_PATH = 'users/registration/'
LOGIN_PATH = 'users/login/'

TEST_USER_NAME = os.getenv('TEST_USER_NAME')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')


@pytest.mark.skip
def test_user_registration():
    ...


@pytest.mark.django_db()
def test_user_authentication_api(
        page: Page,
        context: BrowserContext,
        live_server,
) -> None:
    """Test user authentication api."""
    host = live_server.url

    # get csrf_token
    page.goto(urljoin(host, LOGIN_PATH))
    csrf_token = page.locator('[name="csrfmiddlewaretoken"]').input_value()

    # set post request parameters
    params = {
        'headers': {
            'Referer': host,
            'X-CSRFToken': csrf_token,
        },
        'fail_on_status_code': True,
        'ignore_https_errors': True,
    }
    form = {
        'username': TEST_USER_NAME,
        'password': TEST_PASSWORD,
    }

    # send post request
    post_request: APIRequestContext = context.request
    post_request.post(page.url, **params, form=form)
