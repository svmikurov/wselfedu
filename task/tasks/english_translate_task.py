"""
The English word translate exercise module.

Before beginning a word study exercise, the user defines criteria for
filtering words to study and the order in which they are displayed
during the exercise. These criteria are collected in a
``lookup_conditions``.

``EnglishTranslateExercise`` class takes ``lookup_conditions`` as a
parameter when creating an instance of the class. Class contains the
necessary methods to satisfy these requirements.

The ``task_data`` class property contains all the necessary information
to display the word study exercise to the user.
"""

from random import choice, shuffle

from django.db.models import Q, F
from django.urls import reverse_lazy

from english.models import WordModel
from task.services import LookupParams


class EnglishTranslateExercise:
    """English word translate exercise class.

    Parameters
    ----------
    lookup_conditions : `dict`
        The user exercise conditions.
    """

    # attributes that are assigned a value during initialization
    _user_id = None
    """Current user id (None | `int`).
    """
    _language_order = None
    """The order in which language translations of words are displayed
    (None | `str`).
    """
    timeout = None
    """Time value to display word without translate, sec (None | `int`).
    """
    _lookup_conditions = None
    """The user exercise conditions (None | 'dict').
    """

    # attributes that are assigned a value when calling class methods
    _word_ids = None
    """Identifiers of words that satisfy the conditions of the exercise
    (None | list[int]).
    """
    word_id = None
    """ID of the word rendered to the user in the exercise
    (None | `int`).
    """
    question_text = None
    """The word to be translated in the exercise (None | `str`).
    """
    answer_text = None
    """Translation of the word in the exercise (None | `str`).
    """
    word_count = None
    """A synonym for the length of a verbal expression (None | `str`).
    """
    favorites_url = None
    """URL to call favorite word status update (None | `str`).
    """
    favorites_status = None
    """The status of word is it favorite (None | `bool`)
    """
    knowledge = None
    """The user word knowledge assessment (None | `int`)
    """
    knowledge_url = None
    """URL to call word knowledge assessment update (None | `str`).
    """
    google_translate_word_link = None
    """URL to translate the current word on the Google Translate page.
    (None | `str`).
    """
    word_detail_link = None
    """Link to display detailed information about a word (None | `str`).
    """

    def __init__(self, **lookup_conditions: dict) -> None:
        """Exercise constructor."""
        self._user_id = lookup_conditions.get('user_id')
        self._language_order = lookup_conditions.pop('language_order')
        self.timeout = lookup_conditions.pop('timeout')
        self._lookup_conditions = lookup_conditions

    def create_task(self) -> None:
        """Create task."""
        self._word_ids = self._get_word_ids()
        self.word_id = self._get_random_word_id()
        self._set_task_solution()
        self._set_task_data()

    @property
    def _lookup_params(self) -> tuple[Q]:
        """Word lookup parameters for task (read-only).

        User conditions of the exercise.
        """
        lookup_params = LookupParams(self._lookup_conditions)
        return lookup_params.params

    def _get_word_ids(self) -> list[int]:
        """Make query to database by user conditions of the exercise.

        Returns
        -------
        word_ids : `list[int]`
            List of id word ids that satisfy the conditions of the exercise.

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
                wordsfavoritesmodel__word_id=self.word_id,
            ),
        ).annotate(
            assessment_value=F(
                'worduserknowledgerelation__knowledge_assessment',
            ),
        ).get(
            pk=self.word_id,
        )
        return word

    def _set_task_data(self) -> None:
        """Set data for task rendering."""
        self.word_count = len(self._word_ids)
        self.favorites_status = self._word.favorites_status
        self.favorites_url = reverse_lazy(
            'english:word_favorites_view_ajax',
            kwargs={'word_id': self.word_id},
        )
        self.knowledge = self._word.assessment_value or 0
        self.knowledge_url = reverse_lazy(
            'task:knowledge_assessment',
            kwargs={'word_id': self.word_id},
        )
        self.google_translate_word_link = (
            f'https://translate.google.com/?hl=ru&sl=auto&tl=ru&text='
            f'{self._word.word_eng}&op=translate'
        )
        self.word_detail_link = reverse_lazy(
            'english:words_detail',
            kwargs={'pk': self.word_id},
        )

    @property
    def _word_translation_order(self) -> list[str]:
        """Translations of words in order of user choice
        (`list[str]`, read-only).
        """
        word_translations = [self._word.word_eng, self._word.word_rus]
        if self._language_order == 'EN':
            pass
        elif self._language_order == 'RU':
            word_translations = word_translations[::-1]
        elif self._language_order == 'RN':
            shuffle(word_translations)
        return word_translations

    @property
    def task_data(self) -> dict[str, str | int]:
        """Task data to render to the user.
        (`dict[str, str | int]`, reade-only).
        """
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
            'word_detail_link': self.word_detail_link,
        }
