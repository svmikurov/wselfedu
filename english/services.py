from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from english.models.words import WordsFavoritesModel, WordModel
from users.models import UserModel


def add_word_to_favorites(user_id, word_id, request):
    is_word_already_favorite = WordsFavoritesModel.objects.filter(
        user_id=user_id, word_id=word_id
    ).exists()
    if not is_word_already_favorite:
        WordsFavoritesModel.objects.create(
            user=UserModel.objects.get(pk=user_id),
            word=WordModel.objects.get(pk=word_id),
        )


def remove_word_from_favorites(user_pk, word_pk):
    try:
        word = WordsFavoritesModel.objects.filter(user=user_pk, word=word_pk)
    except ValueError:
        print('Такого слова нет в избранных.')
    else:
        word.delete()


def get_favorites_status(user_id, word_id) -> bool:
    is_word_favorites = WordsFavoritesModel.objects.filter(
        user=user_id, word=word_id
    ).exists()
    return is_word_favorites
