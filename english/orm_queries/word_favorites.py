"""The module of favorite words orm_queries using Django ORM."""

from english.models import WordModel, WordsFavoritesModel
from users.models import UserModel


def is_word_in_favorites(user_id: int | str, word_id: int | str) -> bool:
    """Find out if the word is the favorites.

    Parameters
    ----------
    user_id : `int` | `str`
        The current user id.
    word_id : `int` | `str`
        The word id for status retrieve.

    Returns
    -------
    is_favorites : `bool`
        Return the `True` if the word is the favorites, otherwise return
        the `False`.

    """
    is_favorites = WordsFavoritesModel.objects.filter(
        user=user_id,
        word=word_id,
    ).exists()
    return is_favorites


def update_word_favorites_status(
    word_id: int | str,
    user_id: int | str,
) -> bool:
    """Update the favorite status of the word.

    Parameters
    ----------
    word_id : `int | `str`
        The word id for status update.
    user_id : `int` | `str`
        The current user id.

    Returns
    -------
    favorites_status : `bool`
        Return the `True` if the word is the favorites, otherwise return
        the `False`.

    """
    favorites_status = is_word_in_favorites(user_id, word_id)
    if favorites_status:
        WordsFavoritesModel.objects.filter(user=user_id, word=word_id).delete()
    else:
        WordsFavoritesModel.objects.create(
            user=UserModel.objects.get(pk=user_id),
            word=WordModel.objects.get(pk=word_id),
        )
    favorites_status = is_word_in_favorites(user_id, word_id)
    return favorites_status
