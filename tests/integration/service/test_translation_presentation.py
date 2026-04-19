"""Presentation exercise service tests."""

from typing import Any, Protocol

import pytest

from apps.core.builders.exercise import (
    CaseBuilderProtocol,
    ExerciseCaseBuilder,
)
from apps.core.contracts.entity.exercise import (
    HasExerciseConditions,
    HasExerciseConfig,
)
from apps.core.domains.exercise.deps.protocol import SelectorProtocol
from apps.core.domains.exercise.deps.selector import CandidatesSelector
from apps.core.domains.exercise.dto import ExerciseSpecDTO
from apps.core.domains.exercise.presentation.impl import PresentationDomain
from apps.core.domains.exercise.protocol import (
    Candidates,
    ConditionsProtocol,
    ExerciseConfigProtocol,
    HasCase,
    HasExerciseStatus,
)
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.core.services.exercise.generic import CreateExerciseService
from apps.core.services.exercise.protocol import CreateExerciseProtocol
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translations import (
    UserTranslationsRepository,
)
from apps.users.models import Person


class _SpecProtocol(
    HasExerciseConditions[ConditionsProtocol],
    HasExerciseConfig[ExerciseConfigProtocol],
    Protocol,
):
    """Protocol for exercise parameters service interface."""


class CaseProtocol(Protocol):
    """Protocol core domain case result."""


class _DomainResultProtocol(
    HasExerciseStatus,
    HasCase[CaseProtocol],
    Protocol,
):
    """Protocol for exercise result option interface."""


_Repository = UserRepositoryProtocol[ConditionsProtocol, Candidates]
_Selector = SelectorProtocol[ExerciseConfigProtocol]
# FIXME: Update to protocol
_Domain = PresentationDomain
_ServiceT = CreateExerciseProtocol[_SpecProtocol, _DomainResultProtocol]
_Builder = CaseBuilderProtocol[Any, Any, Any]


@pytest.fixture
def spec() -> _SpecProtocol:
    """Provide service spec parameter."""
    # FIXME: Fix type ignore
    return ExerciseSpecDTO()  # type: ignore


@pytest.fixture
def repository() -> _Repository:
    """Provide translation candidates repository."""
    # FIXME: Fix type ignore
    return UserTranslationsRepository(  # type: ignore
        manager=EnglishTranslation.objects,
    )


@pytest.fixture
def selector() -> _Selector:
    """Provide translation candidates selector."""
    return CandidatesSelector()


@pytest.fixture
def domain(
    selector: _Selector,
) -> _Domain:
    """Provide presentation exercise domain."""
    return PresentationDomain(
        selector=selector,
    )


@pytest.fixture
def builder() -> _Builder:
    """Provide presentation exercise domain DTO builder."""
    return ExerciseCaseBuilder()


@pytest.fixture
def service(
    repository: _Repository,
    domain: _Domain,
    builder: _Builder,
) -> _ServiceT:
    """Provide translation presentation service."""
    return CreateExerciseService(
        candidates_repository=repository,
        domain=domain,
        builder=builder,
    )


class TestTranslationPresentationService:
    """Translation presentation service tests."""

    def test_initialize(
        self,
        service: _ServiceT,
    ) -> None:
        """Test that service has ben initialized successfully."""
        # Act & Assert
        assert service is not None, 'Exercise service was not initialized'

    @pytest.mark.django_db
    def test_execute_success(
        self,
        translations: list[EnglishTranslation],  # populate DB
        user: Person,
        spec: _SpecProtocol,
        service: _ServiceT,
    ) -> None:
        """Test that service call completed successfully."""
        # Act
        case = service.execute(user, spec)

        # Assert
        assert case

        assert case.status
