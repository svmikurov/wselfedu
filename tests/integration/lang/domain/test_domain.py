"""Presentation domain tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.lang import domain, schemas

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.lang import models, repositories, use_cases

    # Dependencies
    type WebUseCase = use_cases.WebPresentationUseCase
    type Repository = repositories.EnglishTranslation
    type Domain = domain.PresentationDomain

    # Data types
    type Translations = list[models.EnglishTranslation]
    type TranslationsQuerySet = QuerySet[models.EnglishTranslation]


class TestTranslationOrder:
    """Translation order tests."""

    @pytest.mark.django_db
    def test_to_native(
        self,
        presentation_domain: Domain,
        translations: Translations,
        translations_queryset: TranslationsQuerySet,
    ) -> None:
        """Apply limit for candidates to translation presentation."""
        first_translation = translations[0]

        settings = schemas.SettingsModel(
            translation_order='to_native',
            word_count=1,
        )
        result, _ = presentation_domain.get_case(
            translations_queryset, settings
        )

        # Assert
        assert result.answer == first_translation.native.word

    @pytest.mark.django_db
    def test_from_native(
        self,
        presentation_domain: Domain,
        translations: Translations,
        translations_queryset: TranslationsQuerySet,
    ) -> None:
        """Apply limit for candidates to translation presentation."""
        first_translation = translations[0]

        settings = schemas.SettingsModel(
            translation_order='from_native',
            word_count=1,
        )
        result, _ = presentation_domain.get_case(
            translations_queryset, settings
        )

        # Assert
        assert result.answer == first_translation.foreign.word


class TestTranslationCount:
    """Translation candidates count tests."""

    @pytest.mark.django_db
    def test_candidates_count(
        self,
        presentation_domain: Domain,
        translations_queryset: TranslationsQuerySet,
    ) -> None:
        """Apply limit for candidates to translation presentation."""
        # Arrange
        translation_count = 4

        # Act
        limit = presentation_domain._get_limit(
            translations_queryset, translation_count
        )

        # Assert
        assert len(limit) == translation_count
