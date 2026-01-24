"""Translation test exercise page."""

from django.utils.translation import gettext as _

from tests.browser.pages import base


class TranslationTestPage(base.BasePage):
    """Translation test exercise page."""

    title = _('lang.page.translation.test.title')
