#
# Этот модуль часть группы сервисов для обработки запросов в базу данных.
#
# Запросы в базу данных осуществляется посредством Django QuerySet API.
#
"""Модуль для отображения Избранных слов в приложении.

Модуль содержит функции запросов в базу данных для добавления, удаления и
запроса, является ли слово избранным пользователем.
Слово может отмечаться пользователем как избранное для отображения на странице
приложения только тех слов, которые отмечены пользователем как избранные.
Пользователь может отметить избранными несколько слов, одно слово может быть
отмечено избранным для нескольких пользователей.
"""

from english.models import WordsFavoritesModel, WordModel
from users.models import UserModel


def is_word_in_favorites(user_id, word_id) -> bool:
    """Return the True if the word is the favorites,
       otherwise return the False.
    """
    is_favorites = WordsFavoritesModel.objects.filter(
        user=user_id, word=word_id,
    ).exists()
    return is_favorites


def update_word_favorites_status(word_id, user_id):
    """Update the status of favorite words."""
    favorites_status = is_word_in_favorites(user_id, word_id)
    if favorites_status:
        WordsFavoritesModel.objects.filter(user=user_id, word=word_id).delete()
    else:
        WordsFavoritesModel.objects.create(
            user=UserModel.objects.get(pk=user_id),
            word=WordModel.objects.get(pk=word_id),
        )
    return not favorites_status
