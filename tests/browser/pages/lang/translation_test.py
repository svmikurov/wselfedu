"""Translation study test browser POM tests."""

from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from .. import base


class TranslationTestPage(base.BasePage):
    """Translation study test browser POM tests."""

    title = _('lang.page.translation.test.title')
    path = str(reverse_lazy('lang:translation_english_test'))
