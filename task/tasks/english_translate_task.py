from random import choice, shuffle

from django.urls import reverse_lazy

from english.models import WordModel
from english.services import (
    create_lookup_params,
    get_knowledge_assessment,
    is_word_in_favorites,
)
from task.services import LookupParams


class EnglishTranslateExercise:
    """English word translate exercise class."""

    success_task = None
    _words = None
    _word_id = None
    word_count = None
    question_text = None
    answer_text = None
    favorites_url = None
    favorites_status = None
    knowledge = None
    knowledge_url = None

    def __init__(
            self,
            *,
            timeout,
            language_order,
            **lookup_conditions,
    ):
        self._user_id = lookup_conditions.get('user_id')
        self.timeout = timeout
        self._language_order = language_order
        self._lookup_conditions = lookup_conditions
        # Create task
        self._create_task()

    def _create_task(self):
        words = self.get_words(self._lookup_params)
        if not words:
            return
        setattr(self, '_words', words)
        setattr(self, 'success_task', True)
        self._set_task_solution()
        self._set_task_data()

    @property
    def _lookup_params(self):
        lookup_params = LookupParams(self._lookup_conditions)
        return lookup_params.params

    @staticmethod
    def get_words(lookup_params):
        """Make user queryset to ``WordModel`` by filter ``lookup_params``."""
        words = WordModel.objects.filter(
            *lookup_params,
        )
        return words

    def _set_task_solution(self):
        """Create and set question and answer text."""
        random_word = choice(self._words)
        word_translations = self._apply_language_order(
            random_word,
            self._language_order,
        )

        setattr(self, '_word_id', random_word.id)
        self.question_text, self.answer_text = word_translations

    def _set_task_data(self):
        favorites_status = is_word_in_favorites(self._user_id, self._word_id)
        knowledge = get_knowledge_assessment(self._word_id, self._user_id)
        favorites_url = reverse_lazy(
            'task:word_favorites_view_ajax',
            kwargs={'word_id': self._word_id},
        )
        knowledge_url = reverse_lazy(
            'task:knowledge_assessment',
            kwargs={'word_id': self._word_id},
        )
        setattr(self, 'word_count', self._words.count())
        setattr(self, 'favorites_url', favorites_url)
        setattr(self, 'favorites_status', favorites_status)
        setattr(self, 'knowledge', knowledge)
        setattr(self, 'knowledge_url', knowledge_url)

    @staticmethod
    def _apply_language_order(word, language_order):
        """Return order of languages by user choice."""
        word_translations = [word.words_eng, word.words_rus]
        if language_order == 'EN':
            pass
        elif language_order == 'RU':
            word_translations = word_translations[::-1]
        elif language_order == 'RN':
            shuffle(word_translations)
        return word_translations
