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


def adapt_lookup_parameters_for_orm(lookup_parameters, lookup_parameters_keys):
    """Адаптируй ключи словаря параметров из request применительно к ORM.

    Parameters:
    -----------
    lookup_parameters : `dict`
        Словарь, чьи ключи надо переименовать.
    lookup_parameters_keys : `dict`
        Словарь, в котором ключ - старое имя ключа, значение - новое имя ключа.

    Return:
    -------
    adapted_lookup_parameters : `dict`
        Адаптированный словарь запросов в бау данных.

    Notes:
    ------
    Переименует именованные в frontend ключи-параметры поиска в соответствии с
    именованием полей в базе данных, согласно lookup_parameters_keys.
    """
    adapted_lookup_parameters = dict()
    for key, value in lookup_parameters.items():
        adapted_key = lookup_parameters_keys.get(key)
        adapted_lookup_parameters[adapted_key] = value
    return adapted_lookup_parameters


def get_lookup_parameters(request, lookup_parameters_keys):
    """Получи из request параметры для поиска в базе данных.

    Переименует именованные в frontend параметры поиска в соответствии с
    именованием полей в базе данных, согласно lookup_parameters.
    """
    pass


def get_random_model_from_queryset(queryset):
    """Получи случайную модель из QuerySet."""
    return choice(list(queryset))
