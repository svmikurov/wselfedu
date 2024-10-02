"""The module of favorite words orm_queries using Django ORM."""

from foreign.models import Word, WordFavorites
from users.models import UserApp


def is_word_in_favorites(user_id: int | str, word_id: int | str) -> bool:
    """Find out if the word is the favorites.

    :param user_id: The current user id.
    :type user_id: `int` | `str`
    :param word_id: The word id for status retrieve.
    :type word_id: `int` | `str`
    :return is_favorites: Return the `True` if the word is the
     favorites, otherwise return the `False`.
    :rtype: `bool`
    """
    is_favorites = WordFavorites.objects.filter(
        user=user_id,
        word=word_id,
    ).exists()
    return is_favorites


def update_word_favorites_status(
    word_id: int | str,
    user_id: int | str,
) -> bool:
    """Update the favorite status of the word.

    :param word_id: The word id for status update.
    :type word_id: `int` | `str`
    :param user_id: The current user id.
    :type user_id: `int` | `str`
    :return favorites_status: Return the `True` if the word is the
     favorites, otherwise return the `False`.
     return the `False`.
    :rtype: `bool`
    """
    favorites_status = is_word_in_favorites(user_id, word_id)
    if favorites_status:
        WordFavorites.objects.filter(user=user_id, word=word_id).delete()
    else:
        WordFavorites.objects.create(
            user=UserApp.objects.get(pk=user_id),
            word=Word.objects.get(pk=word_id),
        )
    favorites_status = is_word_in_favorites(user_id, word_id)
    return favorites_status
