"""Protocol for exercise process parameters adapter."""

from typing import Protocol, TypeVar

from utils.audit.protocol import Auditable

Command_contra = TypeVar('Command_contra', contravariant=True)
Params_contra = TypeVar('Params_contra', contravariant=True)
ExistingCase_contra = TypeVar('ExistingCase_contra', contravariant=True)
Adapted_cov = TypeVar('Adapted_cov', covariant=True)


class ExerciseProcessAdapterProtocol(
    Auditable,
    Protocol[Command_contra, Params_contra, ExistingCase_contra, Adapted_cov],
):
    """Protocol for adapt parameters for exercise process interface."""

    def adapt(
        self,
        command: Command_contra,
        params: Params_contra,
        existing_case: ExistingCase_contra,
    ) -> Adapted_cov:
        """Adapt for exercise process execute."""
