from random import choice, shuffle

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

    def create_task(self) -> None:
        """Create task."""
        self._query_word_ids()
        self._choice_random_word_id()
        self._set_task_solution()

    @property
    def _lookup_params(self) -> tuple[Q]:
        """Word lookup parameters for task."""
        lookup_params = LookupParams(self._lookup_conditions)
        return lookup_params.params

    def _query_word_ids(self) -> None:
        """Make query to database by user conditions of the exercise.

        Set word ids that satisfy the conditions of the exercise (`list[int]`).

        Arguments
        ---------
        _lookup_params : `tuple[Q]`
            User conditions of the exercise.

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
        setattr(self, '_word_ids', word_ids)

    def _choice_random_word_id(self) -> None:
        """Get random word for task."""
        self._word_id = choice(self._word_ids)

    def _set_task_solution(self) -> None:
        """Create and set question and answer text."""
        self._word: WordModel = self._query_word()
        self.question_text, self.answer_text = self._word_translation_order

    def _query_word(self) -> WordModel:
        """Make query to database by word id."""
        word = WordModel.objects.annotate(
            favorites_status=Q(
                wordsfavoritesmodel__user_id=self._user_id,
                wordsfavoritesmodel__word_id=self._word_id,
            ),
        ).annotate(
            assessment_value=F(
                'worduserknowledgerelation__knowledge_assessment',
            ),
        ).get(pk=self._word_id)
        return word

    @property
    def _word_translation_order(self) -> list[str]:
        """Translations of words in order of user choice."""
        # if self._language_order == 'EN':
        word_translations = [self._word.words_eng, self._word.words_rus]
        if self._language_order == 'RU':
            word_translations = word_translations[::-1]
        elif self._language_order == 'RN':
            shuffle(word_translations)
        return word_translations

    @property
    def _word_update_href(self) -> str:
        return reverse_lazy(
            'english:words_update', kwargs={'pk': self._word_id}
        )

    @property
    def _rate_knowledge_url(self) -> str:
        return reverse_lazy(
            'task:knowledge_assessment',
            kwargs={'word_id': self._word_id},
        )

    @property
    def _set_favorites_status_url(self) -> str:
        return reverse_lazy(
            'task:word_favorites_view_ajax',
            kwargs={'word_id': self._word_id},
        )

    @property
    def _google_translate_word_link(self) -> str:
        return (
            f'https://translate.google.com/?hl=ru&sl=auto&tl=ru&text='
            f'{self._word.words_eng}&op=translate'
        )

    @property
    def task_data(self) -> dict[str, str | int]:
        """Task data."""
        return {
            'question_text': self.question_text,
            'answer_text': self.answer_text,
            'timeout': self.timeout,
            'word_count': len(self._word_ids),
            'word_href': self._word_update_href,
            'knowledge': self._word.assessment_value,
            'knowledge_url': self._rate_knowledge_url,
            'favorites_status': self._word.favorites_status,
            'favorites_url': self._set_favorites_status_url,
            'google_translate_word_link': self._google_translate_word_link,
        }
