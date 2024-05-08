from random import choice, shuffle

from django.urls import reverse_lazy

from english.models import WordModel
from english.services import (
    get_knowledge_assessment,
    is_word_in_favorites,
)
from task.services import LookupParams


class EnglishTranslateExercise:
    """English word translate exercise class."""

    def __init__(
            self,
            *,
            timeout,
            language_order,
            **lookup_conditions,
    ):
        self._user_id = lookup_conditions.get('user_id')
        self._language_order = language_order
        self._lookup_conditions = lookup_conditions
        self._word = None
        self._word_id = None
        self.question_text = None
        self.answer_text = None
        self.timeout = timeout
        self.word_count = None
        self.favorites_url = None
        self.favorites_status = None
        self.knowledge = None
        self.knowledge_url = None

    def create_task(self):
        """Create task."""
        word_ids = self.get_word_ids()
        if not word_ids:
            return

        self._word_id = self._get_random_word_id(word_ids)
        self.word_count = len(word_ids)

        self._set_task_solution()
        self._get_task_data()

    @property
    def _lookup_params(self):
        """Word lookup parameters for task."""
        lookup_params = LookupParams(self._lookup_conditions)
        return lookup_params.params

    def get_word_ids(self):
        """Make user queryset to ``WordModel`` by filter ``lookup_params``."""
        word_ids = WordModel.objects.filter(
            *self._lookup_params,
        ).values_list('id', flat=True)
        return word_ids

    @staticmethod
    def _get_random_word_id(word_ids):
        """Get random word for task."""
        return choice(word_ids)

    def _set_task_solution(self):
        """Create and set question and answer text."""
        self._word: WordModel = self._get_word()
        self.question_text, self.answer_text = self._word_translation_order

    def _get_word(self):
        """Get word for task."""
        word = WordModel.objects.get(pk=self._word_id)
        return word

    def _get_task_data(self):
        """Get data for task rendering."""
        self.favorites_status = is_word_in_favorites(
            self._user_id, self._word_id,
        )
        self.knowledge = get_knowledge_assessment(
            self._word_id, self._user_id,
        )
        self.favorites_url = reverse_lazy(
            'task:word_favorites_view_ajax',
            kwargs={'word_id': self._word_id},
        )
        self.knowledge_url = reverse_lazy(
            'task:knowledge_assessment',
            kwargs={'word_id': self._word_id},
        )

    @property
    def _word_translation_order(self):
        """Return order of languages by user choice."""
        word_translations = [self._word.words_eng, self._word.words_rus]
        if self._language_order == 'EN':
            pass
        elif self._language_order == 'RU':
            word_translations = word_translations[::-1]
        elif self._language_order == 'RN':
            shuffle(word_translations)
        return word_translations
