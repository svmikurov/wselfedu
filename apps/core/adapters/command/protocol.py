"""Protocol for assembler's command adapter interface."""

from typing import Protocol, TypeVar, TypeVarTuple, Unpack

Command_contra = TypeVar('Command_contra', contravariant=True)
ArgsT = TypeVarTuple('ArgsT')
Adapted_cov = TypeVar('Adapted_cov', covariant=True)


class CompositeAdapterProtocol(
    Protocol[
        Command_contra,
        Unpack[ArgsT],
        Adapted_cov,
    ],
):
    """Protocol for assembler's command adapter composite interface."""

    def adapt(
        self,
        command: Command_contra,
        *args: Unpack[ArgsT],
    ) -> Adapted_cov:
        """Adapt command with composite parameters."""
