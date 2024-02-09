#
# Этот модуль часть группы задач, выполняемых пользователем.
#
"""Модуль задачи изучения пользователем слов.
"""

from random import shuffle

from english.services.serve_query import (
    get_random_query_from_queryset,
    get_words_for_study,
)


def shuffle_sequence(sequence):
    """Перетасуй последовательность."""
    shuffle(sequence)
    return sequence


def create_task_study_words(lookup_parameters, user_id):
    """Создай задание пользователю для изучения слов, согласно его фильтрам.
    """
    task_study_word = dict()
    words_queryset = get_words_for_study(lookup_parameters, user_id)
    words_length = words_queryset.count()

    if words_queryset:
        word = get_random_query_from_queryset(words_queryset)
        word_translations = [word.words_eng, word.words_rus]
        question, answer = shuffle_sequence(word_translations)

        task_study_word = {
            'word_id': word.id,
            'question': question,
            'answer': answer,
            'words_eng': word.words_eng,
            'words_length': words_length,
        }
    return task_study_word
