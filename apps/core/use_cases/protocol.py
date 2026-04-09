"""Protocol for exercise use case."""

from typing import Protocol, TypeVar

from apps.core.domains.exercise.protocol import (
    HasExerciseConditions,
    HasExerciseConfig,
)

Command_contra = TypeVar('Command_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)


class UseCaseProtocol(Protocol[Command_contra, Result_cov]):
    """Protocol for use case."""

    def execute(
        self,
        command: Command_contra,
    ) -> Result_cov:
        """Execute use case."""


class ResolverProtocol(Protocol[Command_contra, Result_cov]):
    """Protocol for resolver."""

    def resolve(
        self,
        command: Command_contra,
    ) -> Result_cov:
        """Resolve."""


class ExerciseConditions(Protocol):
    """Exercise conditions."""


class ExerciseConfig(Protocol):
    """Exercise configuration."""


class ExerciseParameters(
    HasExerciseConditions[ExerciseConditions],
    HasExerciseConfig[ExerciseConfig],
    Protocol,
):
    """Protocol for exercise parameters."""
