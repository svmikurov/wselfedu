"""Protocol for exercise specification factory interface."""

from typing import Protocol, TypeVar

from utils.audit.protocol import Auditable

Command_contra = TypeVar('Command_contra', contravariant=True)
Params_contra = TypeVar('Params_contra', contravariant=True)
ExistingCase_contra = TypeVar('ExistingCase_contra', contravariant=True)
Spec_cov = TypeVar('Spec_cov', covariant=True)


class ExerciseSpecFactoryProtocol(
    Auditable,
    Protocol[Command_contra, Params_contra, ExistingCase_contra, Spec_cov],
):
    """Protocol for exercise specification factory interface."""

    def create(
        self,
        command: Command_contra,
        params: Params_contra,
        case: ExistingCase_contra,
    ) -> Spec_cov:
        """Cerate the exercise specification."""
