"""English word translation test that awards points."""
from functools import cached_property
from random import choices, shuffle

from english.models import WordModel
from task.tasks import EnglishTranslateExercise

NUMBER_OF_TRANSLATION_OPTIONS = 7
"""Number of translation options offered in the test (`int`)
"""


class EnglishTranslateTestExercise(EnglishTranslateExercise):
    """English translate test exercise."""

    @cached_property
    def translation_order(self) -> list[str]:
        """"""
        word_translations = ['eng_word', 'rus_word']
        if self._language_order == 'EN':
            pass
        elif self._language_order == 'RU':
            # ruff: noqa: TD002, TD003
            # TODO: Try ``reverse`` method.
            word_translations = word_translations[::-1]
        elif self._language_order == 'RN':
            shuffle(word_translations)
        return word_translations

    @property
    def translate_options(self):
        """Translate options (`list[int]`, reade-only)."""
        translate_into_language_index = -1
        language_word = self.translation_order[translate_into_language_index]
        translate_option_ids = choices(self._word_ids)

        translate_options = WordModel.objects.filter(
            pk__in=translate_option_ids,
        ).values(language_word)
        return translate_options
