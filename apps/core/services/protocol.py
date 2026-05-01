"""Protocol for service interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from utils.audit.protocol import Auditable

if TYPE_CHECKING:
    from apps.users.models import Person

Spec_contra = TypeVar('Spec_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)


class UserServiceProtocol(
    Auditable,
    Protocol[Spec_contra, Result_cov],
):
    """Protocol for user's service."""

    def execute(self, user: Person, spec: Spec_contra) -> Result_cov:
        """Execute."""
