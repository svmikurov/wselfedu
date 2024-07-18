import os
from typing import Generator
from unittest import TestCase

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT')


class PageFixtureTestCase(StaticLiveServerTestCase):
    """Test with Playwright Pytest page fixture class
     using StaticLiveServerTestCase.

    The page fixture is set in the test function scope.

    Example
    -------
    Use to get an authorized page:

        class TestPage(PageFixtureTestCase):

            fixtures = ['tests_e2e/fixtures/fixture-db-user']

            def setUp(self):
                authorize_the_page(self.page, self.live_server_url)
                self.page.goto(self.live_server_url)
    """

    @pytest.fixture(autouse=True)
    def run_around_tests(self) -> Generator[None, None, None]:
        """Get new Playwright Pytest page fixture."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        yield
        self.browser.close()
        self.playwright.stop()

    @classmethod
    def setUpClass(cls) -> None:
        """Allow Django to use async in class scope.

        Sets ``DJANGO_ALLOW_ASYNC_UNSAFE`` to `true`, which allows
        Django to use async at class scope.
        """
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
        super().setUpClass()

    @property
    def site_host(self):
        """Page host schema."""
        return self.live_server_url


class StageTestCase(TestCase):
    """Test class using Playwright Pytest page fixture in Stage
    environment."""

    @property
    def site_host(self):
        """Page host schema."""
        return os.getenv('HOST')


pom_test_classes = {
    'development': PageFixtureTestCase,
    'stage': StageTestCase,
}
"""Base classes for the derived class POMBaseTest (`dict`).
Each is used in its own testing environment.
"""
pom_test_class = pom_test_classes.get(ENVIRONMENT, 'development')
"""Current representation of the test environment base class.
"""


class POMBaseTest(pom_test_class):
    """Base class for testing Page Object Model instance page."""
