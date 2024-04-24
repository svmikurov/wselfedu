from random import choice, shuffle

from contrib_app.task.base_subject import BaseSubject
from english.models import WordModel


class _TranslateSubject(BaseSubject):
    """English word translate subject class.

    Examples:
    ---------
    translate_subject.set_subject_params()
    """

    def _set_task_solution(self):
        """Create and set question and answer text."""
        words = WordModel.objects.all()
        random_word = choice(words)
        word = [random_word.words_eng, random_word.words_rus]
        shuffle(word)

        self._question_text, self._answer_text = word


translate_subject = _TranslateSubject()
