from random import choice, shuffle

from contrib_app.task.base_subject import BaseSubject
from english.models import WordModel


class _TranslateSubject(BaseSubject):
    """English word translate subject class."""

    def _set_task_solution(self):
        """Create and set question and answer text."""
        words = WordModel.objects.all()
        random_word = choice(words)
        word_translations = [random_word.words_eng, random_word.words_rus]
        shuffle(word_translations)

        self._question_text, self._answer_text = word_translations

    def __str__(self):
        return 'Перевод слов'

    @property
    def subject_name(self):
        """Get subject name."""
        return 'translate_subject'


translate_subject = _TranslateSubject()
