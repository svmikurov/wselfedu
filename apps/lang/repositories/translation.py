"""English translation repository."""

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple, override

from django.db import transaction

from .. import models
from . import abc as base

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.core import models as core_models
    from apps.users.models import Person


class _TranslationWords(NamedTuple):
    """Native and foreign words of translation."""

    native: models.NativeWord
    english: models.EnglishWord


def _normalize_word(word: str) -> str:
    """Normalize word."""
    return word.strip('?!#- .,').lower()


class TranslationRepository(base.TranslationRepoABC):
    """English translation repository."""

    @override
    @transaction.atomic
    def create(
        self,
        user: Person,
        native: str,
        english: str,
        category: models.LangCategory,
        source: core_models.Source,
        marks: QuerySet[models.LangMark],
        normalize: bool = True,
    ) -> None:
        """Create english translation."""
        words = self._get_or_create_words(user, native, english, normalize)

        translation, _ = models.EnglishTranslation.objects.get_or_create(
            user=user,
            native=words.native,
            english=words.english,
            category=category,
            source=source,
        )

        if marks:
            translation.marks.set(marks)

    @override
    @transaction.atomic
    def update(
        self,
        user: Person,
        instance: models.EnglishTranslation,
        native: str,
        english: str,
        category: models.LangCategory,
        source: core_models.Source,
        marks: QuerySet[models.LangMark],
        normalize: bool = True,
    ) -> None:
        """Update english translation."""
        words = self._get_or_create_words(user, native, english, normalize)

        instance.native = words.native
        instance.english = words.english
        instance.category = category
        instance.source = source
        instance.marks.set(marks)
        instance.save()

    @override
    def get_translation_id(
        self,
        native_id: int,
    ) -> int:
        """Get english translation relationship by native word ID."""
        return models.EnglishTranslation.objects.get(native=native_id).pk

    @override
    def get_translations(
        self,
        user: Person,
    ) -> QuerySet[models.EnglishTranslation]:
        """Get english translations."""
        return models.EnglishTranslation.objects.filter(
            user=user,
        )

    @staticmethod
    def _get_or_create_words(
        user: Person,
        native: str,
        english: str,
        normalize: bool = True,
    ) -> _TranslationWords:
        """Get or create native and foreign words for translation."""
        native_to_store = native
        english_to_store = english

        if normalize:
            native_to_store = _normalize_word(native)
            english_to_store = _normalize_word(english)

        native_obj, _ = models.NativeWord.objects.get_or_create(
            user=user,
            word=native_to_store,
        )
        english_obj, _ = models.EnglishWord.objects.get_or_create(
            user=user,
            word=english_to_store,
        )
        return _TranslationWords(native_obj, english_obj)
