"""Protocol for use case interface."""

from typing import Protocol, TypeVar

from utils.audit.protocol import Auditable

Params_contra = TypeVar('Params_contra', contravariant=True)
Context_contra = TypeVar('Context_contra', contravariant=True)
Validated_contra = TypeVar('Validated_contra', contravariant=True)
CommandData_cov = TypeVar('CommandData_cov', covariant=True)


class AssemblerProtocol(
    Protocol[
        Params_contra,
        Context_contra,
        Validated_contra,
        CommandData_cov,
    ],
):
    """Protocol for assembler interface."""

    def prepare(
        self,
        params: Params_contra,
        context: Context_contra,
        data: Validated_contra,
    ) -> CommandData_cov:
        """Prepare request data for use case execute."""


class AuditableAssemblerProtocol(
    Auditable,
    AssemblerProtocol[
        Params_contra,
        Context_contra,
        Validated_contra,
        CommandData_cov,
    ],
):
    """Protocol for auditable assembler interface."""
