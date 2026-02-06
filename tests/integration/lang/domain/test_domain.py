"""Presentation domain tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from apps.core.domain.exercise import DisplayOrder, PresentationDomain
from apps.lang import schemas

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from apps.lang import handlers, models, repositories

    # Dependencies
    type WebUseCase = handlers.WebPresentationUseCase
    type Repository = repositories.TranslationConditionsRepository
    type Domain = PresentationDomain

    # Data types
    type Translations = list[models.EnglishTranslation]
    type TranslationsQuerySet = QuerySet[models.EnglishTranslation]


class TestTranslationOrder:
    """Translation order tests."""

    # DEPRECATED: Delete or update after refactoring complete
    @pytest.mark.skip('Deprecated')
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
            display_order=DisplayOrder.EXPLAIN,
            item_count=1,
        )
        result, _ = presentation_domain.execute(
            translations_queryset,  # type: ignore
            settings,  # type: ignore
        )

        # Assert
        assert result.answer_text == first_translation.native.word

    # DEPRECATED: Delete or update after refactoring complete
    @pytest.mark.skip('Deprecated')
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
            display_order=DisplayOrder.DEFINE,
            item_count=1,
        )
        result, _ = presentation_domain.execute(
            translations_queryset,  # type: ignore
            settings,  # type: ignore
        )

        # Assert
        assert result.answer_text == first_translation.foreign.word


# DEPRECATED: Delete or update after refactoring complete
@pytest.mark.skip('Deprecated')
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
        limit = presentation_domain._get_limited(
            # TODO: Fix type ignore
            translations_queryset,  # type: ignore
        )

        # Assert
        assert len(limit) == translation_count
