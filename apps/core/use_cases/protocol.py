"""Protocol for exercise use case."""

from typing import Protocol, TypeVar

Command_contra = TypeVar('Command_contra', contravariant=True)
Configuration_cov = TypeVar('Configuration_cov', covariant=True)


class ExerciseConfigurationResolverProtocol(
    Protocol[Command_contra, Configuration_cov]
):
    """Protocol for exercise configuration resolver."""

    def resolve(
        self,
        command: Command_contra,
    ) -> Configuration_cov:
        """Get exercise configuration."""
