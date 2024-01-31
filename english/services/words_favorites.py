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

from english.models.words import WordsFavoritesModel, WordModel
from users.models import UserModel


def add_word_to_favorites(user_id, word_id):
    """Add word to favorites.
    """
    is_word_already_favorite = WordsFavoritesModel.objects.filter(
        user_id=user_id, word_id=word_id,
    ).exists()
    if not is_word_already_favorite:
        WordsFavoritesModel.objects.create(
            user=UserModel.objects.get(pk=user_id),
            word=WordModel.objects.get(pk=word_id),
        )


def remove_word_from_favorites(user_pk, word_pk):
    """Remove word from favorites.
    """
    try:
        word = WordsFavoritesModel.objects.filter(user=user_pk, word=word_pk)
    except ValueError:
        print('Такого слова нет в избранных.')
    else:
        word.delete()


def is_word_in_favorites(user_id, word_id) -> bool:
    """Return the True if the word is the favorites,
       otherwise return the False.
    """
    is_favorites = WordsFavoritesModel.objects.filter(
        user=user_id, word=word_id,
    ).exists()
    return is_favorites


def update_words_favorites_status(word_id, user_id, favorites_action):
    """Измени статус слова, избранное ли оно.

    Если слова нет среди избранных - добавляет слово в избранные,
    если слово среди избранных - убирает слово из избранных.
    """
    # Не используется значение favorites_action = "change",
    # во избежание дополнительного запроса в БД - текущий статус слова
    if favorites_action == 'add':
        add_word_to_favorites(user_id, word_id)
    elif favorites_action == 'remove':
        remove_word_from_favorites(user_id, word_id)
