"""Protocol for assembler's command adapter interface."""

from typing import Protocol, TypeVar, TypeVarTuple, Unpack

Command_contra = TypeVar('Command_contra', contravariant=True)
CompositeParams = TypeVarTuple('CompositeParams')
Adapted_cov = TypeVar('Adapted_cov', covariant=True)


class CompositeAdapterProtocol(
    Protocol[
        Command_contra,
        Unpack[CompositeParams],
        Adapted_cov,
    ],
):
    """Protocol for assembler's command adapter composite interface."""

    def adapt(
        self,
        command: Command_contra,
        *params: Unpack[CompositeParams],
    ) -> Adapted_cov:
        """Adapt command with composite parameters."""
