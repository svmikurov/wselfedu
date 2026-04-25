"""Presentation exercise service tests."""

from typing import Any, Protocol

import pytest
from django.db.models import QuerySet

from apps.core.builders.exercise import ExerciseCaseBuilder
from apps.core.builders.protocol import ExerciseTaskBuilderProtocol
from apps.core.domains.exercise.deps.protocol import SelectorProtocol
from apps.core.domains.exercise.deps.selector import CandidatesSelector
from apps.core.domains.exercise.presentation.impl import PresentationDomain
from apps.core.domains.exercise.protocol import (
    ConditionsProtocol,
    ExerciseConfigProtocol,
    HasCase,
)
from apps.core.repositories.protocol import UserRepositoryProtocol
from apps.core.services.exercise.generic import CreateExerciseService
from apps.core.services.exercise.protocol import CreateExerciseProtocol
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translations import (
    UserTranslationsRepository,
)
from apps.users.models import Person
from interfaces.aliases import CandidatesAlias
from interfaces.protocols.domain.exercise import (
    HasExerciseStatus,
)
from interfaces.protocols.domain.params import (
    HasConditions,
    HasConfig,
)
from interfaces.schemas.domain.exercise.params import (
    ExerciseSpecDTO,
)


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


_Repository = UserRepositoryProtocol[
    ConditionsProtocol,
    CandidatesAlias,
]
_TranslationRepository = UserRepositoryProtocol[
    ConditionsProtocol,
    QuerySet[EnglishTranslation, EnglishTranslation],
]
_Selector = SelectorProtocol[ExerciseConfigProtocol]
# FIXME: Update to protocol
_Domain = PresentationDomain
_ServiceT = CreateExerciseProtocol[_SpecProtocol, _DomainResultProtocol]
_Builder = ExerciseTaskBuilderProtocol[Any, Any, Any]


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
