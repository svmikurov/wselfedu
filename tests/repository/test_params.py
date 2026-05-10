"""Presentation parameters repository tests."""

import pytest

from apps.lang.models import (
    ExerciseConditions,
    PresentationSettings,
    TranslationConfiguration,
)
from apps.lang.repositories.exercise.params.translation_presentation import (
    RegularTranslationPresentationRepository,
)
from apps.users.models import Person
from contracts.schemas.base import NullDTO
from interfaces.protocols.domain.exercise import (
    ConditionsProtocol,
    ExerciseConfigProtocol,
    ExerciseParametersProtocol,
    ExerciseSettingsProtocol,
)
from ports.contract.entity.general import NullProtocol
from ports.contract.infra.repository import RepositoryProtocol

_RepositoryT = RepositoryProtocol[NullProtocol, ExerciseParametersProtocol]


@pytest.fixture
def repository() -> _RepositoryT:
    """Provide presentation parameters repository."""
    return RegularTranslationPresentationRepository(
        conditions_manager=ExerciseConditions.objects,
        config_manager=PresentationSettings.objects,
        settings_manager=TranslationConfiguration.objects,
    )


# TODO: Add missing test
class TestRepository:
    """Presentation parameters repository tests."""

    def test_repository_initialized_success(
        self,
        repository: _RepositoryT,
    ) -> None:
        """Test that repository has been initialized successfully."""
        assert repository is not None, 'Repository was not initialized'

    @pytest.mark.django_db
    def test_return_params_dto(
        self,
        user: Person,
        repository: _RepositoryT,
        db_translation_lockup_conditions: ConditionsProtocol,
        db_presentation_settings: ExerciseSettingsProtocol,
        db_exercise_configuration: ExerciseConfigProtocol,
    ) -> None:
        """Test that returns correct exercise parameters DTO."""
        # Act
        params = repository.fetch(user, NullDTO())

        # Assert
        assert params.conditions == db_translation_lockup_conditions
        assert params.conf == db_exercise_configuration
        assert params.settings == db_presentation_settings


# IDEA:
@pytest.mark.django_db
class TestExerciseParameters:
    """Exercise parameters DTO test."""

    def test_create_conditions(
        self,
        db_translation_lockup_conditions: ConditionsProtocol,
    ) -> None:
        """Test create translation conditions."""
        # Act & Assert
        # Created in database successfully.
        assert db_translation_lockup_conditions

    def test_create_configuration(
        self,
        db_presentation_settings: ExerciseConfigProtocol,
    ) -> None:
        """Test create translation conditions."""
        # Act & Assert
        # Created in database successfully.
        assert db_presentation_settings

    def test_create_settings(
        self,
        db_exercise_configuration: ExerciseSettingsProtocol,
    ) -> None:
        """Test create translation conditions."""
        # Act & Assert
        # Created in database successfully.
        assert db_exercise_configuration
