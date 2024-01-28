#
# Этот модуль часть группы задач, выполняемых пользователем.
#
"""Модуль задачи изучения пользователем слов.
"""

from random import shuffle

from english.models import WordModel
from english.services.serve_query import filter_objects, get_random_model_from_queryset

LOOKUP_PARAMETERS = {
    'words_favorites': 'favorites__pk',
    'category_id': 'category_id',
    'source_id': 'source_id',
    'word_count': 'word_count__in',
    'assessment': 'worduserknowledgerelation__knowledge_assessment__in',
    'user': 'worduserknowledgerelation__user_id',
}
"""Константа переименования ключей kwargs, полученных из requests, в ключи
lookup_parameters для получения изучаемых слов (`dict`)"""

LANGUAGE_KEYS = ['words_eng', 'words_rus']
"""Константа ключей к модели слова для для изучения (`list`)"""


def get_lookup_parameters(request, lookup_parameters_keys):
    """Получи из request параметры для поиска в базе данных.

    Переименует именованные в frontend параметра поиска в соответствии с
    именованием полей в базе данных, согласно lookup_parameters.
    """
    pass


def shuffle_sequence(sequence):
    shuffle(sequence)
    return sequence


def create_task_study_words(request):
    model_manager = WordModel.objects
    lookup_parameters = get_lookup_parameters(request, LOOKUP_PARAMETERS)
    words_queryset = filter_objects(model_manager, **lookup_parameters)
    random_word_task = get_random_model_from_queryset(words_queryset)
    question_key, answer_key = shuffle_sequence(LANGUAGE_KEYS)

    task_study_words = {
        'word_id': random_word_task.get(id),
        'question': random_word_task.get(question_key),
        'answer': random_word_task.get(answer_key),
    }
    return task_study_words
