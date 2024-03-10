#
# Этот модуль часть группы сервисов для обработки запросов в базу данных.
#
"""Модуль для получения слова из базы данных в упражнении "Изучаем слова".
"""
import copy
from random import choice

import datetime
from datetime import date, timedelta

from django.db.models import Subquery, QuerySet
from django.utils import timezone

from english.models import WordModel, WordUserKnowledgeRelation
from english.services.word_knowledge_assessment import get_numeric_value


def get_date_value(form_value: str) -> date:
    """Преобразуй строковое обозначение периода в дату.

    Если текстовое значение даты не задано, возвращает дату добавления
    пользователем первого слова.
    """
    day_today = datetime.datetime.now(tz=timezone.utc)
    # Определение начала периода, по дате добавления первого слова.
    begin_date_period = WordModel.objects.order_by('created_at').first(
    ).created_at

    if form_value == 'DT':
        model_date = day_today
    elif form_value == 'D3':
        model_date = day_today - timedelta(days=3)
    elif form_value == 'W1':
        model_date = day_today - timedelta(weeks=1)
    elif form_value == 'W4':
        model_date = day_today - timedelta(weeks=4)
    elif form_value == 'NC':
        model_date = begin_date_period
    else:
        raise ValueError('Выбранный период не предусмотрен.')

    return model_date


def collect_params(lookup_params, lookup_method, param_value):
    """Добавь текущий параметр поиска к имеющимся, если он имеет значение.
    """
    if param_value:
        lookup_params[lookup_method] = param_value
    return lookup_params


def create_lookup_params(form_data: dict, user_id=None) -> dict:
    """Создай параметры поиска слов в базе данных.
    """
    lookup_params = dict()

    # Фильтр избранных слов по пользователю.
    param_value = form_data['favorites']
    lookup_method = 'favorites__pk'
    if param_value and user_id:
        lookup_params[lookup_method] = user_id

    # Фильтр по id категории.
    category_id = int(form_data['category'])
    lookup_method = 'category_id'
    lookup_params = collect_params(lookup_params, lookup_method, category_id)

    # Фильтр по id источника.
    source_id = int(form_data['source'])
    lookup_method = 'source_id'
    lookup_params = collect_params(lookup_params, lookup_method, source_id)

    # Фильтр по периоду добавления (изменения) слова.
    period_start_date = get_date_value(form_data['period_start_date'])
    period_end_date = get_date_value(form_data['period_end_date'])
    lookup_params['created_at__range'] = (
        period_start_date.strftime('%Y-%m-%d 00:00:00+00:00'),
        period_end_date.strftime('%Y-%m-%d 23:59:59+00:00'),
    )

    # Фильтр по длине выражения из слов.
    word_count = form_data['word_count']
    if 'NC' not in word_count:
        word_count += ['NC']
    lookup_method = 'word_count__in'
    lookup_params[lookup_method] = word_count

    # Фильтр по оценке пользователем уровня знания слова (этапу изучения).
    knowledge_assessment = form_data['knowledge_assessment']
    # Строковое значение "уровня знания" преобразуется в диапазон чисел.
    nums_range = get_numeric_value(knowledge_assessment)
    lookup_method = 'worduserknowledgerelation__knowledge_assessment__in'
    lookup_params = collect_params(lookup_params, lookup_method, nums_range)

    return lookup_params


def get_random_query_from_queryset(queryset):
    """Get a random model from a QuerySet."""
    return choice(queryset)


def get_words_for_study(lookup_params: dict, user_id: int) -> QuerySet | None:
    """Retrieve words based on a specific user's search parameters.

    Parameters
    ----------
    lookup_params : Dict[str, str | int | sequence]
        Where:
        dict key - lookup method (e.g. `category_id` or `word_count__in`);
        dict value - lookup criterion (e.g. `2` or `['OW', 'CB', 'NC']`).
    user_id : int
        User ID.

    Returns
    -------
    words : `QuerySet` | None
        `QuerySet` of word filtered by lookup_params for study words task.
        None if user not chosen knowledge assessment.
    """
    # Извлекаем из параметров поиска параметр поиска по оценке пользователем
    # уровня знания слова.
    params = copy.deepcopy(lookup_params)
    try:
        knowledge_assessment_value: list = params.pop(
            'worduserknowledgerelation__knowledge_assessment__in'
        )
    except KeyError:
        return None

    # Применяем фильтры.
    words = WordModel.objects.filter(**params)
    words = words.filter(
        worduserknowledgerelation__knowledge_assessment__in=Subquery(
            WordUserKnowledgeRelation.objects.filter(
                knowledge_assessment__in=knowledge_assessment_value
            ).values('knowledge_assessment'),
        ),
        worduserknowledgerelation__user_id__exact=user_id,
    ).filter(
        user_id=user_id,
    )

    # Вновь добавленные слова не имеют оценок пользователя, и поэтому, не
    # учтены в таблице worduserknowledgerelation.
    # Получаем слова, не отображенные в таблице worduserknowledgerelation.
    not_assessment_words = WordModel.objects.exclude(
        pk__in=Subquery(
            WordUserKnowledgeRelation.objects.all().values('word_id'),
        ),
        worduserknowledgerelation__user_id__exact=user_id,
    ).filter(
        **params,
    ).filter(
        user_id=user_id,
    )

    # Объединим слова с оценками уровня знания пользователя и без.
    study_knowledge_assessment = 1
    if study_knowledge_assessment in knowledge_assessment_value:
        words |= not_assessment_words

    return words
