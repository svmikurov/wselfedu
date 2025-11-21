"""Create word translation."""

from typing import NamedTuple, override

from django.db import transaction
from django.db.models.query import QuerySet

from apps.users.models import CustomUser

from .. import models
from . import abc as base


class TranslationParams(NamedTuple):
    """Get translation params."""

    user: CustomUser
    marks: list[models.LangMark] | None


class Translations(NamedTuple):
    """English word translations."""

    pk: int
    native: models.NativeWord
    english: models.EnglishWord


def normalize_word(word: str) -> str:
    """Normalize word."""
    return word.strip('?!#- .,').lower()


class TranslationRepo(base.TranslationRepoABC):
    """Create English word translation."""

    @override
    @transaction.atomic
    def create_translation(
        self,
        user: CustomUser,
        native: str,
        english: str,
        normalize: bool = True,
    ) -> base.CreationStatus:
        """Create English word translation."""
        native_to_store = native
        english_to_store = english

        if normalize:
            native_to_store = normalize_word(native)
            english_to_store = normalize_word(english)

        native_obj, native_created = models.NativeWord.objects.get_or_create(
            user=user,
            word=native_to_store,
        )
        english_obj, english_created = (
            models.EnglishWord.objects.get_or_create(
                user=user,
                word=english_to_store,
            )
        )
        _, translation_created = (
            models.EnglishTranslation.objects.get_or_create(
                user=user,
                native=native_obj,
                english=english_obj,
            )
        )
        return base.CreationStatus(
            native_created,
            english_created,
            translation_created,
        )

    @override
    def get_translation_id(
        self,
        word_id: int,
    ) -> int:
        """Get word translation relationship."""
        return models.EnglishTranslation.objects.get(native=word_id).pk

    def get_translations(
        self,
        params: TranslationParams | None = None,
    ) -> QuerySet[models.EnglishTranslation]:
        """Get English word translations."""
        return models.EnglishTranslation.objects.all()
