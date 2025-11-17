"""Create word translation."""

from typing import override

from django.db import transaction

from apps.users.models import CustomUser

from .. import models
from . import abc as base


def normalize_word(word: str) -> str:
    """Normalize word."""
    return word.strip()


class TranslationRepo(base.TranslationRepoABC):
    """Create English word translation."""

    @override
    @transaction.atomic
    def create_translation(
        self,
        user: CustomUser,
        native: str,
        english: str,
    ) -> base.CreationStatus:
        """Create English word translation."""
        native_obj, native_created = models.NativeWord.objects.get_or_create(
            user=user,
            word=normalize_word(native),
        )
        english_obj, english_created = (
            models.EnglishWord.objects.get_or_create(
                user=user,
                word=normalize_word(english),
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
