"""Service protocol."""

from typing import Protocol, TypeVar

from apps.users.models import Person

Spec_contra = TypeVar('Spec_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)


class ServiceProtocol(Protocol[Spec_contra, Result_cov]):
    """Protocol for service."""

    def execute(self, user: Person, spec: Spec_contra) -> Result_cov:
        """Execute."""
