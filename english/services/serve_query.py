#
# Этот модуль часть группы сервисов для обработки запросов в базу данных.
#
# Запросы в базу данных осуществляется посредством Django QuerySet API.
#
"""Модуль для запросов в базу данных.

Используется для единого применения в представлениях.
"""
from random import choice

from django.db.models import Manager


def get_objects(objects: Manager, **kwargs):
    """Получи объект от менеджера модели"""
    return objects.get(**kwargs)


def all_objects(objects: Manager):
    """Получи все объекты от менеджера модели"""
    return objects.all()


def filter_objects(objects: Manager, *args, **kwargs):
    """Примени фильтр к менеджеру модели"""
    return objects.filter(*args, **kwargs)


def get_random_model_from_queryset(queryset):
    """Получи случайную модель из QuerySet"""
    return choice(list(queryset))
