"""Protocol for exercise process parameters adapter."""

from typing import Protocol, TypeVar

Command_contra = TypeVar('Command_contra', contravariant=True)
Params_contra = TypeVar('Params_contra', contravariant=True)
CurrentCase_contra = TypeVar('CurrentCase_contra', contravariant=True)
Adapted_cov = TypeVar('Adapted_cov', covariant=True)


class ExerciseProcessAdapterProtocol(
    Protocol[Command_contra, Params_contra, CurrentCase_contra, Adapted_cov]
):
    """Protocol for adapt parameters for exercise process interface."""

    def adapt(
        self,
        command: Command_contra,
        params: Params_contra,
        current_case: CurrentCase_contra,
    ) -> Adapted_cov:
        """Adapt for exercise process execute."""
