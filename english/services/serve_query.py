#
# Этот модуль часть группы сервисов для обработки запросов в базу данных.
#
# Запросы в базу данных осуществляется посредством Django QuerySet API.
#
"""Модуль для запросов в базу данных.
"""
from random import choice

import datetime
from datetime import timedelta
from django.utils import timezone

from english.models import WordModel
from english.services.words_knowledge_assessment import get_numeric_value


def create_lookup_parameters(querydict):
    """Получи из request параметры для запроса слов в базе данных.

    Ожидаются изменения в условиях поиска по периоду добавления (изменения)
    слова, после добавления формы в представление.

    Формирует словарь фильтров для запроса слов из базы данных.
    """
    lookup_parameters = dict()

    # Фильтр по избранным словам.
    # Преобразует тип значения [str] в int.
    words_favorites = querydict.get('words_favorites')
    if words_favorites and words_favorites != ['']:
        lookup_parameters[
            'favorites__pk'
        ] = int(words_favorites[0])

    # Фильтр по категории.
    # Преобразует тип значения [str] в int.
    category = querydict.get('category_id')
    if category and category != ['']:
        lookup_parameters[
            'category_id'
        ] = int(category[0])

    # Фильтр по источнику.
    # Преобразует тип значения [str] в int.
    source = querydict.get('source_id')
    if source and source != ['']:
        lookup_parameters[
            'source_id'
        ] = int(source[0])

    # Фильтр по количеству слов.
    # Всегда присутствуют слова, количество которых не установлено: ['NC'].
    word_count = querydict.get('word_count', [])
    if word_count and word_count != ['']:
        lookup_parameters[
            'word_count__in'
        ] = querydict.get('word_count') + ['NC']

    # Фильтр по оценке знаний.
    # Строковое значение "уровня знания" преобразуется в диапазон чисел.
    if querydict.get('assessment'):
        lookup_parameters[
            'worduserknowledgerelation__knowledge_assessment__in'
        ] = get_numeric_value(
            querydict.get('assessment')
        )

    # Фильтр по периоду добавления (изменения) слова.
    period = {
        'start_period': querydict.get('start_period', ['9'])[0],
        'end_period': querydict.get('end_period', ['1'])[0],
    }

    print(f'\nlookup_parameters = {lookup_parameters}')

    day_today = datetime.datetime.now(tz=timezone.utc)
    begin_date_period = (
        WordModel.objects.order_by('updated_at').first().updated_at
    )
    for key, value in period.items():
        if value == '1':
            period[key] = day_today
        elif value == '2':
            period[key] = day_today - timedelta(days=3)
        elif value == '3':
            period[key] = day_today - timedelta(weeks=1)
        elif value == '4':
            period[key] = day_today - timedelta(weeks=4)
        elif value == '9':
            period[key] = begin_date_period
        else:
            raise ValueError('Выбранный период не предусмотрен.')

    # Программно добавляется часовой пояс '%Y-%m-%d 00:00:00+00:00'.
    # Добавляется в целях прохождения тестов.
    # Возможно, будет удалено программное добавление '00:00:00+00:00'.
    lookup_parameters['updated_at__range'] = (
        period['start_period'].strftime('%Y-%m-%d 00:00:00+00:00'),
        period['end_period'].strftime('%Y-%m-%d 23:59:59+00:00'),
    )
    print(f'\nlookup_parameters = {lookup_parameters}')

    return lookup_parameters


def get_random_query_from_queryset(queryset):
    """Получи случайную модель из QuerySet."""
    return choice(queryset)
