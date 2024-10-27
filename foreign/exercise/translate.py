"""The Foreign word translate exercise.

Before beginning a word study exercise, the user defines criteria for
filtering words to study and the order in which they are displayed
during the exercise. These criteria are collected in a
``lookup_conditions``.

``ForeignWordTranslateExercise`` class takes ``lookup_conditions`` as a
parameter when creating an instance of the class. Class contains the
necessary methods to satisfy these requirements.

The ``task_data`` class property contains all the necessary information
to display the word study exercise to the user.
"""

from random import shuffle

from django.db.models import F
from django.urls import reverse_lazy

from config.constants import (
    DEFAULT_LANGUAGE_ORDER,
    FROM_NATIVE,
    RANDOM,
    TO_NATIVE,
)
from contrib.exercise import ExerciseData
from foreign.models import Word, WordFavorites, WordProgress
from foreign.queries.lookup_params import WordLookupParams
from users.models import UserApp


class TranslateExerciseGUI(ExerciseData):
    """Foreign word translate GUI app exercise.

    GUI application exercise.
    """

    model = Word
    lookup_params = WordLookupParams

    def __init__(self, lookup_conditions: dict) -> None:
        """Exercise constructor."""
        self.language_order = lookup_conditions.pop(
            'language_order', DEFAULT_LANGUAGE_ORDER
        )
        super().__init__(lookup_conditions)

    def create_task(self) -> None:
        """Create task."""
        super().create_task()
        self.question_text, self.answer_text = self._word_translation_order()

    def _word_translation_order(self) -> list[str]:
        """Get translation of words in order of user choice
        (`list[str]`, read-only).
        """  # noqa:  D205
        word_translations = [self.item.foreign_word, self.item.native_word]
        if self.language_order == TO_NATIVE:
            pass
        elif self.language_order == FROM_NATIVE:
            word_translations = word_translations[::-1]
        elif self.language_order == RANDOM:
            shuffle(word_translations)
        return word_translations

    def _query_item_progress(self) -> int:
        """Query the word progress study assessment.

        :return: Word progress study assessment.
        :rtype: int
        """
        default_progress_value = 0
        queryset = WordProgress.objects.filter(
            user=UserApp.objects.get(pk=self.lookup_conditions['user_id']),
            word=self.item,
        )
        # WordProgress model instance exist if the user assessed the
        # level of knowledge of the word.
        try:
            progress = int(queryset.last().progress)
        except AttributeError:
            progress = default_progress_value
        return progress


class TranslateExercise(TranslateExerciseGUI):
    """Foreign word translate exercise class.

    Browser application exercise.
    """

    def __init__(self, lookup_conditions: dict) -> None:
        """Exercise constructor."""
        self._user_id = lookup_conditions.get('user_id')
        self.timeout = lookup_conditions.pop('timeout')
        super().__init__(lookup_conditions)

    @property
    def task_data(self) -> dict[str, str | int]:
        """Task data to render to the user
        (`dict[str, str | int]`, reade-only).
        """  # noqa:  D205
        self.create_task()
        return {
            'word_id': self.item.pk,
            'question_text': self.question_text,
            'answer_text': self.answer_text,
            'timeout': self.timeout,
            'word_count': len(self.item_ids),
            'progress': Word.objects.annotate(
                progress_value=F('wordprogress__progress'),
            ).get(pk=self.item.pk).progress_value or 0,
            'knowledge_url': reverse_lazy(
                'foreign:progress',
                kwargs={'word_id': self.item.pk},
            ),
            'favorites_status': WordFavorites.objects.filter(
                word=self.item, user=self.item.user
            ).exists(),
            'favorites_url': reverse_lazy(
                'foreign:word_favorites_view_ajax',
                kwargs={'word_id': self.item.pk},
            ),
            'google_translate_word_link': (
                f'https://translate.google.com/?hl=ru&sl=auto&tl=ru&text='
                f'{self.item.foreign_word}&op=translate'
            ),
            'word_detail_link': reverse_lazy(
                'foreign:words_detail',
                kwargs={'pk': self.item.id},
            ),
        }  # fmt: skip
