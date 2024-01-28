#
# Этот модуль часть группы задач, выполняемых пользователем.
#
"""Модуль задачи изучения пользователем слов.
"""

from random import shuffle

from english.models import WordModel
from english.services.serve_query import (
    filter_objects,
    get_random_model_from_queryset,
)

LANGUAGE_KEYS = ['words_eng', 'words_rus']
"""Константа ключей к языкам модели слова для изучения (`list`)"""


def get_lookup_parameters(request, lookup_parameters_keys):
    """Получи из request параметры для поиска в базе данных.

    Переименует именованные в frontend параметры поиска в соответствии с
    именованием полей в базе данных, согласно lookup_parameters.
    """
    pass


def shuffle_sequence(sequence):
    shuffle(sequence)
    return sequence


def create_task_study_words(lookup_parameters):
    model_manager = WordModel.objects
    words_queryset = filter_objects(model_manager, **lookup_parameters)
    random_word_task = get_random_model_from_queryset(words_queryset)
    question_key, answer_key = shuffle_sequence(LANGUAGE_KEYS)

    task_study_word = {
        'word_id': random_word_task.get(id),
        'question': random_word_task.get(question_key),
        'answer': random_word_task.get(answer_key),
    }
    return task_study_word
