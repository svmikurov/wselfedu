"""Create word translation."""

from typing import NamedTuple

from django.db import transaction

from apps.users.models import CustomUser

from ..models import EnglishTranslation, EnglishWord, NativeWord


def normalize_word(word: str) -> str:
    """Normalize word."""
    return word.strip()


class CreationStatus(NamedTuple):
    """Status of create English word translation."""

    created_native: bool
    created_english: bool
    created_translation: bool


class CreateEnglishTranslation:
    """Create English word translation."""

    @transaction.atomic
    def create_translation(
        self,
        user: CustomUser,
        native: str,
        english: str,
    ) -> CreationStatus:
        """Create English word translation."""
        native_obj, native_created = NativeWord.objects.get_or_create(
            user=user,
            word=normalize_word(native),
        )
        english_obj, english_created = EnglishWord.objects.get_or_create(
            user=user,
            word=normalize_word(english),
        )
        _, translation_created = EnglishTranslation.objects.get_or_create(
            user=user,
            native=native_obj,
            english=english_obj,
        )
        return CreationStatus(
            native_created,
            english_created,
            translation_created,
        )
