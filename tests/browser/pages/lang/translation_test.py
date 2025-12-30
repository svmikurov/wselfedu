"""Translation study test browser POM tests."""

from django.urls import reverse_lazy

from .. import base


class TranslationTestPage(base.BasePage):
    """Translation study test browser POM tests."""

    title = 'Словарный тест'
    path = str(reverse_lazy('lang:translation_english_test'))
