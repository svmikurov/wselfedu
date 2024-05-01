from random import choice, shuffle

from django.urls import reverse_lazy

from english.services import (
    get_words_for_study,
    create_lookup_params,
    get_knowledge_assessment,
    is_word_in_favorites,
)


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
            user_id,
            timeout,
            language_order,
            **lookup_conditions,
    ):
        self._user_id = user_id
        self.timeout = timeout
        self._language_order = language_order
        self._lookup_conditions = lookup_conditions
        # Create task
        self._create_task()

    def _create_task(self):
        self._set_words()
        if self._words:
            self._set_task_solution()
            self._set_task_data()
            setattr(self, 'success_task', True)

    @property
    def _lookup_params(self):
        return create_lookup_params(self._lookup_conditions, self._user_id)

    def _set_words(self, ):
        words = get_words_for_study(self._lookup_params, self._user_id)
        setattr(self, '_words', words)

    def _set_task_solution(self):
        """Create and set question and answer text."""
        random_word = choice(self._words)
        word_translations = [random_word.words_eng, random_word.words_rus]
        shuffle(word_translations)

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
