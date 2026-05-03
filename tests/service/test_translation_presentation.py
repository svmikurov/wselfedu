"""Presentation exercise service tests."""

from ast import TypeVar
from typing import Any, Protocol, TypeAlias

import pytest

from apps.core.builders.exercise.case import ExerciseCaseBuilder
from apps.core.builders.protocol import SpecDtoBuilderProtocol
from apps.core.domains.exercise.deps.protocol import SelectorProtocol
from apps.core.domains.exercise.deps.selector import CandidatesSelector
from apps.core.domains.exercise.presentation.impl import PresentationDomain
from apps.core.domains.exercise.protocol import (
    ConditionsProtocol,
    ExerciseConfigProtocol,
    HasCase,
)
from apps.core.repositories.protocol import RepositoryProtocol
from apps.core.services.exercise.generic import CreateExerciseService
from apps.core.services.exercise.protocol import ExerciseServiceProtocol
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translations import (
    UserTranslationsRepository,
)
from apps.users.models import Person
from contracts import aliases
from contracts.entity.domain.exercise.fields import (
    HasExerciseStatus,
)
from contracts.entity.domain.params import (
    HasConditions,
    HasConfig,
)
from contracts.schemas.domain.exercise.params import (
    ExerciseSpecDTO,
)
from interfaces.schemas.domain.exercise import TaskItem


class _SpecProtocol(
    HasConditions[ConditionsProtocol],
    HasConfig[ExerciseConfigProtocol],
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


CaseT = TypeVar('CaseT')
_Candidates: TypeAlias = list[TaskItem]
_Repository = RepositoryProtocol[
    ConditionsProtocol,
    aliases.CandidatesAlias,
]
_TranslationRepository = RepositoryProtocol[ConditionsProtocol, _Candidates]
_Selector = SelectorProtocol[ExerciseConfigProtocol]
_Domain = aliases.ExerciseDomainAlias
_ServiceT = ExerciseServiceProtocol[_SpecProtocol, _DomainResultProtocol]
_Builder = SpecDtoBuilderProtocol[Any, Any, Any]


@pytest.fixture
def spec() -> _SpecProtocol:
    """Provide service spec parameter."""
    # FIXME: Fix type ignore
    return ExerciseSpecDTO()  # type: ignore


@pytest.fixture
def repository() -> _TranslationRepository:
    """Provide translation candidates repository."""
    return UserTranslationsRepository(
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
    return PresentationDomain(  # type: ignore
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
        builder=builder,  # type: ignore
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
        translations: list[TaskItem],  # populate DB
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
