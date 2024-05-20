from random import choice, shuffle
from typing import Any

from django.db.models import Q, F
from django.urls import reverse_lazy

from english.models import WordModel
from task.services import LookupParams


class EnglishTranslateExercise:
    """English word translate exercise class."""

    def __init__(self, **lookup_conditions):
        self._user_id = lookup_conditions.get('user_id')
        self._language_order = lookup_conditions.pop('language_order')
        self.timeout = lookup_conditions.pop('timeout')
        self._lookup_conditions = lookup_conditions
        self._word_ids = None
        self._word_id = None
        self._word = None
        self.question_text = None
        self.answer_text = None
        self.word_count = None
        self.favorites_url = None
        self.favorites_status = None
        self.knowledge = None
        self.knowledge_url = None
        self.google_translate_word_link = None

    def create_task(self) -> None:
        """Create task."""
        self._word_ids = self._get_word_ids()
        self._word_id = self._get_random_word_id()
        self._set_task_solution()
        self._set_task_data()

    @property
    def _lookup_params(self) -> tuple[Q]:
        """Word lookup parameters for task."""
        lookup_params = LookupParams(self._lookup_conditions)
        return lookup_params.params

    def _get_word_ids(self) -> list[int]:
        """Make query to database by user conditions of the exercise.

        Arguments
        ---------
        _lookup_params : `tuple[Q]`
            User conditions of the exercise.

        Returns
        -------
        word_ids : `list[int]`
            List of id words that satisfy the conditions of the exercise.

        Raises
        ------
        ValueError
            Raised if no words that satisfy the conditions of the exercise.
        """
        word_ids = WordModel.objects.filter(
            *self._lookup_params,
        ).values_list('id', flat=True)

        if not word_ids:
            raise ValueError('No words found to the specified conditions')
        return word_ids

    def _get_random_word_id(self) -> int:
        """Get random word for task."""
        return choice(self._word_ids)

    def _set_task_solution(self) -> None:
        """Create and set question and answer text."""
        self._word: WordModel = self._get_word()
        self.question_text, self.answer_text = self._word_translation_order

    def _get_word(self) -> WordModel:
        """Get word for task."""
        word = WordModel.objects.annotate(
            favorites_status=Q(
                wordsfavoritesmodel__user_id=self._user_id,
                wordsfavoritesmodel__word_id=self._word_id,
            ),
        ).annotate(
            assessment_value=F(
                'worduserknowledgerelation__knowledge_assessment',
            ),
        ).get(
            pk=self._word_id,
        )
        return word

    def _set_task_data(self) -> None:
        """Get data for task rendering."""
        self.word_count = len(self._word_ids)
        self.favorites_status = self._word.favorites_status
        self.favorites_url = reverse_lazy(
            'task:word_favorites_view_ajax',
            kwargs={'word_id': self._word_id},
        )
        self.knowledge = self._word.assessment_value or 0
        self.knowledge_url = reverse_lazy(
            'task:knowledge_assessment',
            kwargs={'word_id': self._word_id},
        )
        self.google_translate_word_link = (
            f'https://translate.google.com/?hl=ru&sl=auto&tl=ru&text='
            f'{self._word.word_eng}&op=translate'
        )

    @property
    def _word_translation_order(self) -> list[str]:
        """Translations of words in order of user choice."""
        word_translations = [self._word.word_eng, self._word.word_rus]
        if self._language_order == 'EN':
            pass
        elif self._language_order == 'RU':
            word_translations = word_translations[::-1]
        elif self._language_order == 'RN':
            shuffle(word_translations)
        return word_translations

    @property
    def task_data(self) -> dict[str, Any]:
        """Dictionary with task data."""
        return {
            'question_text': self.question_text,
            'answer_text': self.answer_text,
            'timeout': self.timeout,
            'word_count': self.word_count,
            'knowledge': self.knowledge,
            'knowledge_url': self.knowledge_url,
            'favorites_status': self.favorites_status,
            'favorites_url': self.favorites_url,
            'google_translate_word_link': self.google_translate_word_link,
        }
