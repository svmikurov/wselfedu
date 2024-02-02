#
# Этот модуль часть группы задач, выполняемых пользователем.
#
"""Модуль задачи изучения пользователем слов.
"""

from random import shuffle

from english.models import WordModel
from english.services.serve_query import get_random_query_from_queryset


def shuffle_sequence(sequence):
    """Перетасуй последовательность."""
    shuffle(sequence)
    return sequence


def create_task_study_words(lookup_parameters):
    """Создай задание пользователю для изучения слов, согласно его фильтрам.
    """
    task_study_word = dict()
    include_parameters, exclude_parameters = lookup_parameters
    words_queryset = WordModel.objects.filter(
        **include_parameters
    ).exclude(
        **exclude_parameters,
    )

    if words_queryset:
        word = get_random_query_from_queryset(words_queryset)
        word_translations = [word.words_eng, word.words_rus]
        question, answer = shuffle_sequence(word_translations)

        task_study_word = {
            'word_id': word.id,
            'question': question,
            'answer': answer,
            'words_eng': word.words_eng
        }
    return task_study_word
