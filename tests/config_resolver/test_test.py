"""Test exercise configuration resolver tests."""

import pytest

from apps.lang.models import ExerciseConditions, TranslationConfiguration
from apps.lang.repositories.legacy.exercise.conditions import (
    RegularParametersRepository,
)
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
)
from interfaces.protocols.domain.exercise import ExerciseParametersProtocol
from kernel.resolver.config_resolver import (
    ExerciseConfigurationResolver,
)
from ports.contract.entity.general import NullProtocol
from ports.contract.enums.exercise import ExerciseKind
from ports.contract.infra.repository import RepositoryProtocol
from ports.contract.infra.reslover import ResolverProtocol
from ports.interfaces.protocols.command import UserCommandProtocol

RepositoryT = RepositoryProtocol[
    NullProtocol,
    ExerciseParametersProtocol,
]
ResolverT = ResolverProtocol[
    UserCommandProtocol,
    ExerciseParametersProtocol,
]


@pytest.fixture
def parameters_repository() -> RepositoryT:
    """Provide user configuration repository."""
    return RegularParametersRepository(
        parameters_manager=ExerciseConditions.objects,
        conf_manager=TranslationConfiguration.objects,
    )


# HACK: Update return type hint to protocol
@pytest.fixture
def default_parameters() -> ExerciseParametersDTO:
    """Provide default user's exercise configuration."""
    return ExerciseParametersDTO()


@pytest.fixture
def resolver(
    parameters_repository: RepositoryT,
    default_parameters: ExerciseParametersProtocol,
) -> ResolverT:
    """Provide exercise configuration resolver."""
    return ExerciseConfigurationResolver(
        exercise_type=ExerciseKind.TEST,
        parameters_repository=parameters_repository,
        default=default_parameters,
    )


class TestParametersResolver:
    """Exercise configuration resolver tests."""

    def test_initialized(self, resolver: ResolverT) -> None:
        """Test that resolver initialized successfully."""
        assert resolver is not None
