#
# Этот модуль часть группы сервисов для обработки запросов в базу данных.
#
# Запросы в базу данных осуществляется посредством Django QuerySet API.
#
"""Модуль для запросов в базу данных.
"""
from random import choice

from english.services.words_knowledge_assessment import get_numeric_value

LOOKUP_PARAMETERS_KEYS = {
    'words_favorites': 'favorites__pk',
    'category_id': 'category_id',
    'source_id': 'source_id',
    'word_count': 'word_count__in',
    'assessment': 'worduserknowledgerelation__knowledge_assessment__in',
    'user_id': 'worduserknowledgerelation__user_id',
}
"""Константа переименования ключей kwargs, полученных из requests, в ключи
lookup_parameters для получения изучаемых слов (`dict`)"""

KEYS_WITH_INT_VALUE = {'words_favorites', 'category_id', 'source_id'}
"""Параметры поиска для запросов в базу данных, значения которых должны быть
целым числом.
"""


def get_lookup_parameters(querydict):
    """Получи из request параметры для поиска слов в базе данных.

    Адаптирует полученные данные к работе с ОРМ.
    """
    lookup_parameters = dict()

    for key, value in querydict.items():

        # Преобразуй строковое представление "уровня знания" в диапазон чисел
        # для этого уровня
        if key == 'assessment':
            value = get_numeric_value(value)

        # Включи в параметры поиска 'Любое количество слов' - добавлять везде
        # Возможно, эта опция будет удалена в будущем.
        # Без этой опции из формирования задачи выпадают слова,
        # при добавлении в словарь которых не выбрано "количество солов".
        if key == 'word_count':
            value += ['NC']

        if value != [''] and key in LOOKUP_PARAMETERS_KEYS:
            lookup_key = LOOKUP_PARAMETERS_KEYS[key]

            if key in KEYS_WITH_INT_VALUE:
                value = int(value[0])

            lookup_parameters[lookup_key] = value

    return lookup_parameters


def get_random_query_from_queryset(queryset):
    """Получи случайную модель из QuerySet."""
    return choice(queryset)
