"""Base Playwright POM test."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import pytest
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from playwright.sync_api import sync_playwright

from apps.users.models import Person

if TYPE_CHECKING:
    from playwright.sync_api import Browser, BrowserContext, Page, Playwright


class _Test(StaticLiveServerTestCase):
    """Base Playwright POM test."""

    playwright: Playwright
    browser: Browser
    _page: Page

    @classmethod
    def setUpClass(cls) -> None:
        """Start the Playwright and launch the browser."""
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
        super().setUpClass()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch()

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop the playwright and close the browser."""
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()


class BaseTest(_Test):
    """Base Playwright POM test for not authenticated user."""

    def setUp(self) -> None:
        """Set up page with base url."""
        self._page = self.browser.new_page(base_url=str(self.live_server_url))


class BaseAuthTest(_Test):
    """Base Playwright POM test for authenticated user."""

    context: BrowserContext
    user: Person

    @pytest.fixture(autouse=True)
    def set_user(self, user: Person) -> None:
        """Set user."""
        self.user = user

    def setUp(self) -> None:
        """Set up the authenticated browser session.

        Creates an authenticated browser session without going through
        the login UI. This approach is faster than filling out login
        forms and allows testing authenticated pages directly.
        """
        # Create a new Django session store for authentication.
        session = SessionStore()
        session.create()

        # Manually set authentication data in the session.
        # This mimics what Django's login() function does internally.
        session['_auth_user_id'] = str(self.user.pk)
        session['_auth_user_backend'] = (
            'django.contrib.auth.backends.ModelBackend'
        )
        session['_auth_user_hash'] = self.user.get_session_auth_hash()

        # Save session to database.
        session.save()

        # Create a new Playwright browser context
        # with the test server URL as base.
        # Contexts provide isolated sessions
        # (cookies, localStorage, etc.)
        self.context = self.browser.new_context(
            base_url=str(self.live_server_url)
        )

        # Parse the live server URL
        # to extract hostname for cookie domain.
        parsed_url = urlparse(str(self.live_server_url))

        # Inject the Django session cookie into the browser context.
        # This makes the browser appear as
        # "logged in" to the Django application.
        self.context.add_cookies(
            [
                {
                    'name': settings.SESSION_COOKIE_NAME,
                    'value': session.session_key,  # type: ignore[typeddict-item]
                    'domain': parsed_url.hostname,
                    # Cookie valid for all paths on the domain
                    'path': '/',
                    # Note: secure, httpOnly, sameSite
                    # omitted for test simplicity.
                    # In production tests,
                    # these should match your settings.
                }
            ]
        )

        # Create a new page (browser tab)
        # within the authenticated context.
        # All pages created from this context
        # will share the same authentication.
        self._page = self.context.new_page()
