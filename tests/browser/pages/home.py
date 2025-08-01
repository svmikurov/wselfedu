"""Defines Home page gor POM browser testing."""

from tests.browser.pages.base import BasePage


class HomePage(BasePage):
    """Home page."""

    title = 'WSE Главная'
    path = '/'
