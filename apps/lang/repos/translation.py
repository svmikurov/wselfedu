"""Create word translation."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from django.db import transaction

from .. import models
from . import abc as base

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.users.models import Person

    from .. import models


def normalize_word(word: str) -> str:
    """Normalize word."""
    return word.strip('?!#- .,').lower()


class TranslationRepo(base.TranslationRepoABC):
    """Create English word translation."""

    @override
    @transaction.atomic
    def create_translation(
        self,
        user: Person,
        native: str,
        english: str,
        normalize: bool = True,
    ) -> None:
        """Create English word translation."""
        native_to_store = native
        english_to_store = english

        if normalize:
            native_to_store = normalize_word(native)
            english_to_store = normalize_word(english)

        native_obj, _ = models.NativeWord.objects.get_or_create(
            user=user,
            word=native_to_store,
        )
        english_obj, _ = models.EnglishWord.objects.get_or_create(
            user=user,
            word=english_to_store,
        )
        _, _, = (
            models.EnglishTranslation.objects.get_or_create(
                user=user,
                native=native_obj,
                english=english_obj,
            )
        )

    @override
    def get_translation_id(
        self,
        word_id: int,
    ) -> int:
        """Get word translation relationship."""
        return models.EnglishTranslation.objects.get(native=word_id).pk

    @override
    def get_translations(
        self,
        user: Person,
    ) -> QuerySet[models.EnglishTranslation]:
        """Get English word translations."""
        return models.EnglishTranslation.objects.filter(
            user=user,
        )
