from random import choice, shuffle

from english.services import get_words_for_study, create_lookup_params
from task.task.base_subject import BaseSubject


class _TranslateSubject(BaseSubject):
    """English word translate subject class."""

    def __init__(self):
        super().__init__()
        self.word_id = None
        self._user_id = None
        self._lookup_params = None
        self._language_order = None

    def apply_subject(self, *, user_id, language_order, **task_conditions):
        """"""
        lookup_params = create_lookup_params(task_conditions, user_id)

        setattr(self, '_user_id', user_id)
        setattr(self, '_language_order', language_order)
        setattr(self, '_lookup_params', lookup_params)
        super().apply_subject()

    def _set_task_solution(self):
        """Create and set question and answer text."""
        word_qs = get_words_for_study(self._lookup_params, self._user_id)
        random_word = choice(word_qs)
        word_translations = [random_word.words_eng, random_word.words_rus]
        shuffle(word_translations)

        setattr(self, 'word_id', random_word)
        self._question_text, self._answer_text = word_translations

    def __str__(self):
        return 'Перевод слов'

    @property
    def subject_name(self):
        """Get subject name."""
        return 'translate_subject'


translate_subject = _TranslateSubject()
