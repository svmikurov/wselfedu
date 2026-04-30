"""Protocol for factory interface."""

from typing import Protocol, TypeVar

Spec_contra = TypeVar('Spec_contra', contravariant=True)
Result_co = TypeVar('Result_co', covariant=True)


class FactoryProtocol(Protocol[Spec_contra, Result_co]):
    """Protocol for factory interface."""

    def build(self, spec: Spec_contra) -> Result_co:
        """Build."""
