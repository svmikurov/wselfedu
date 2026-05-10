"""Presentation exercise service tests."""

from ast import TypeVar
from typing import Any, Protocol, TypeAlias

import pytest

from apps.core.repositories.protocol import RepositoryProtocol
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translations import (
    UserTranslationsRepository,
)
from apps.users.models import Person
from contracts import aliases
from contracts.entity.domain.exercise.fields import (
    HasCase,
    HasExerciseStatus,
)
from contracts.entity.domain.params import (
    HasConditions,
    HasConfig,
)
from contracts.infra.domain.selector import SelectorProtocol
from contracts.schemas.domain.exercise.params import (
    ExerciseSpecDTO,
)
from interfaces.protocols.domain.exercise import (
    CandidatesT,
    ConditionsProtocol,
    ExerciseConfigProtocol,
)
from interfaces.schemas.domain.exercise import TaskItem
from kernel.domain.exercise import CandidatesSelector, PresentationDomain
from kernel.formatter.exercise import PresentationFormatter
from kernel.service.exercise import CreateExerciseService
from ports.contract.infra.formatter import ConfFormatterProtocol
from ports.contract.infra.service import UserSpecServiceProtocol


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
    CandidatesT,
]
_TranslationRepository = RepositoryProtocol[ConditionsProtocol, _Candidates]
_Selector = SelectorProtocol[ExerciseConfigProtocol]
_Domain = aliases.ExerciseDomainAlias
_ServiceT = UserSpecServiceProtocol[_SpecProtocol, _DomainResultProtocol]
_Formatter = ConfFormatterProtocol[Any, Any, Any]


@pytest.fixture
def spec() -> _SpecProtocol:
    """Provide service spec parameter."""
    return ExerciseSpecDTO()


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
    return PresentationDomain(
        selector=selector,
    )


@pytest.fixture
def formatter() -> _Formatter:
    """Provide presentation exercise domain DTO builder."""
    return PresentationFormatter()


@pytest.fixture
def service(
    repository: _Repository,
    domain: _Domain,
    formatter: _Formatter,
) -> _ServiceT:
    """Provide translation presentation service."""
    return CreateExerciseService(
        candidates_repository=repository,
        domain=domain,
        formatter=formatter,
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
