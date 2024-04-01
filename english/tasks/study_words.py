#
# Этот модуль часть группы задач, выполняемых пользователем.
#
"""Модуль задачи изучения пользователем слов.
"""

from random import shuffle

from django.db.models import QuerySet

from english.services.serve_query import (
    get_random_query_from_queryset,
    get_words_for_study,
)


def shuffle_sequence(sequence):
    """Перетасуй последовательность."""
    shuffle(sequence)
    return sequence


def create_task_study_words(lookup_params: dict, user_id: int) -> dict | None:
    """Create a task for the user to learn words using his filters."""
    task_study_word = None
    words: QuerySet = get_words_for_study(lookup_params, user_id)

    if words:
        word_count = words.count()
        word = get_random_query_from_queryset(words)
        word_translations = [word.words_eng, word.words_rus]
        question, answer = shuffle_sequence(word_translations)

        task_study_word = {
            'word_id': word.id,
            'question': question,
            'answer': answer,
            'word_eng': word.words_eng,
            'word_count': word_count,
            'source': word.source.name if word.source else '',
        }
    return task_study_word
