"""Presentation parameters repository tests."""

from typing import Any, TypeVar

import pytest

from apps.core.domains.exercise.protocol import GenericExerciseParameters
from apps.core.domains.null import NullDTO
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.lang.models import (
    ExerciseConditions,
    PresentationConfig,
    TranslationSetting,
)
from apps.lang.repositories.exercise.params.translation_presentation import (
    RegularTranslationPresentationRepository,
)
from apps.users.models import Person

ExerciseTypeConfigT = TypeVar('ExerciseTypeConfigT')
ExerciseSettingsT = TypeVar('ExerciseSettingsT')

_FilterT = Any
_ParametersT = GenericExerciseParameters[
    Any,
    Any,
    Any,
]
_RepositoryT = UserRepositoryProtocol[_FilterT, _ParametersT]


@pytest.fixture
def repository() -> UserRepositoryProtocol[_FilterT, _ParametersT]:
    """Provide presentation parameters repository."""
    return RegularTranslationPresentationRepository(
        conditions_manager=ExerciseConditions.objects,
        config_manager=PresentationConfig.objects,
        settings_manager=TranslationSetting.objects,
    )


class TestRepository:
    """Presentation parameters repository tests."""

    def test_repository_initialized_success(
        self,
        repository: _RepositoryT,
    ) -> None:
        """Test that repository has been initialized successfully."""
        assert repository is not None, 'Repository was not initialized'

    @pytest.mark.django_db
    def test_fetch(
        self,
        user: Person,
        repository: _RepositoryT,
    ) -> None:
        """Test fetch parameters."""
        # Act & Assert
        assert repository.fetch(user, NullDTO())
