"""Presentation UseCase tests via DI container."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.http import QueryDict

from apps.core import exceptions
from apps.lang.di.handler.exercise.presentation import (
    TranslationPresentationContainer,
)

if TYPE_CHECKING:
    from apps.lang import handlers, models
    from apps.users.models import Person

    type Container = TranslationPresentationContainer
    type WebUseCase = handlers.WebPresentationUseCase
    type Translations = list[models.EnglishTranslation]


class TestUseCaseContainer:
    """Presentation UseCase tests via DI container."""

    # DEPRECATED: Delete or update after refactoring complete
    @pytest.mark.skip('Deprecated')
    @pytest.mark.django_db
    def test_execute_without_conditions(
        self,
        user: Person,
        web_use_case: WebUseCase,
        translations: Translations,  # Populate DB
    ) -> None:
        """Get all translations without lookup conditions."""
        assert web_use_case.execute(user, QueryDict()) is not None

    # DEPRECATED: Delete or update after refactoring complete
    @pytest.mark.skip('Deprecated')
    @pytest.mark.django_db
    def test_no_translations_available_exception(
        self,
        user: Person,
        web_use_case: WebUseCase,
    ) -> None:
        """Raises exception when no translations."""
        with pytest.raises(exceptions.NoTranslationsAvailableException):
            assert web_use_case.execute(user, QueryDict())

    def test_create_container(self) -> None:
        """Create use case DI container."""
        assert TranslationPresentationContainer() is not None
