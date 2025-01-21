"""The module of favorite words orm_queries using Django ORM."""

from foreign.models import Word, WordFavorites
from users.models import UserApp


def is_word_in_favorites(user_id: int | str, word_id: int | str) -> bool:
    """Find out if the word is the favorites."""
    is_favorites = WordFavorites.objects.filter(
        user=user_id,
        word=word_id,
    ).exists()
    return is_favorites


def update_word_favorites_status(
    word_id: int | str, user_id: int | str
) -> bool:
    """Update the favorite status of the word."""
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
