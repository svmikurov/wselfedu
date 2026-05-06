"""Language use cases DI container test."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from apps.lang.di.use_case.container import LangUseCaseContainer
    from di import MainContainer


@pytest.fixture
def use_cases(main_container: MainContainer) -> LangUseCaseContainer:
    """Provide lang app use cases DI container."""
    return main_container.lang.use_cases  # type: ignore


class TestLanguageUseCasesContainers:
    """Test lang app exercise DI containers."""

    def test_create_use_cases_container(
        self,
        use_cases: LangUseCaseContainer,
    ) -> None:
        """Test that lang app use cases DI container initialized."""
        assert use_cases is not None, (
            'Language app *use cases* container was not initialized'
        )


class TestCreateExerciseUseCase:
    """Test create exercise use case."""

    def test_create_regular_translation_presentation_use_case_success(
        self,
        use_cases: LangUseCaseContainer,
    ) -> None:
        """Test that process presentation handler initialized."""
        assert use_cases.regular_translation_presentation is not None, (
            'Language app *regular translation use cases* was not initialized'
        )
