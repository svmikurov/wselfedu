"""Defines Home page gor POM browser testing."""

from django.utils.translation import gettext as _

from tests.browser.pages.base import BasePage


class HomePage(BasePage):
    """Home page."""

    title = _('home.page.title')
    path = '/'
