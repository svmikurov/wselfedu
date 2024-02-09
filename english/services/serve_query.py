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

from django.db.models import Subquery
from django.utils import timezone

from english.models import WordModel, WordUserKnowledgeRelation
from english.services.words_knowledge_assessment import get_numeric_value, \
    MAX_KNOWLEDGE_ASSESSMENT


def create_lookup_parameters(querydict) -> tuple:
    """Получи из request параметры для запроса слов в базе данных.

    Ожидаются изменения в условиях поиска по периоду добавления (изменения)
    слова, после добавления формы в представление.

    Возвращает кортеж фильтров для запроса слов из базы данных, содержащий
    параметры для включения и параметры для исключения слов в запросе.
    """
    include_parameters = dict()
    exclude_parameters = dict()

    # Фильтр по избранным словам.
    # Преобразует тип значения [str] в int.
    words_favorites = querydict.get('words_favorites')
    if words_favorites and words_favorites != ['']:
        include_parameters[
            'favorites__pk'
        ] = int(words_favorites[0])

    # Фильтр по категории.
    # Преобразует тип значения [str] в int.
    category = querydict.get('category_id')
    if category and category != ['']:
        include_parameters[
            'category_id'
        ] = int(category[0])

    # Фильтр по источнику.
    # Преобразует тип значения [str] в int.
    source = querydict.get('source_id')
    if source and source != ['']:
        include_parameters[
            'source_id'
        ] = int(source[0])

    # Фильтр по количеству слов.
    # Всегда присутствуют слова, количество которых не установлено: ['NC'].
    word_count = querydict.get('word_count', [])
    if word_count and word_count != ['']:
        include_parameters[
            'word_count__in'
        ] = querydict.get('word_count') + ['NC']

    # Фильтр исключений по оценке знаний.
    # Строковое значение "уровня знания" преобразуется в диапазон чисел.
    # Через разницу множеств вычисляется оценки для исключения.
    assessment = querydict.get('assessment')
    if assessment:
        all_assessments = set(
            (num for num in range(0, MAX_KNOWLEDGE_ASSESSMENT + 1))
        )
        include_assessments = set(get_numeric_value(assessment))
        exclude_assessments = list(all_assessments - include_assessments)
        exclude_parameters[
            'worduserknowledgerelation__knowledge_assessment__in'
        ] = sorted(exclude_assessments)

    # Фильтр по периоду добавления (изменения) слова.
    period = {
        'start_period': querydict.get('start_period', ['9'])[0],
        'end_period': querydict.get('end_period', ['1'])[0],
    }
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
    include_parameters['updated_at__range'] = (
        period['start_period'].strftime('%Y-%m-%d 00:00:00+00:00'),
        period['end_period'].strftime('%Y-%m-%d 23:59:59+00:00'),
    )

    lookup_parameters = (include_parameters, exclude_parameters)
    return lookup_parameters


def get_random_query_from_queryset(queryset):
    """Получи случайную модель из QuerySet."""
    return choice(queryset)


def get_words_for_study(lookup_parameters, user_id):
    objects = WordModel.objects
    include_parameters, exclude_parameters = lookup_parameters

    words = objects.filter(**include_parameters)
    if exclude_parameters:
        words.filter(
            worduserknowledgerelation__knowledge_assessment__in=Subquery(
                WordUserKnowledgeRelation.objects.exclude(
                    knowledge_assessment__in=exclude_parameters.get(
                        'worduserknowledgerelation__knowledge_assessment__in'
                    )
                ).values('knowledge_assessment')
            ),
            worduserknowledgerelation__user_id__exact=user_id,
        )
    return words
