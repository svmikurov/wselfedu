"""Protocol for service interface."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, TypeVar

from ports.interfaces.protocols.domain import (
    ExerciseConfigProtocol,
)
from ports.interfaces.protocols.service import (
    PresentationCaseProtocol,
    TestCaseProtocol,
)
from utils.audit.protocol import Auditable

if TYPE_CHECKING:
    from apps.users.models import Person

Spec_contra = TypeVar('Spec_contra', contravariant=True)
Result_cov = TypeVar('Result_cov', covariant=True)


class UserSpecServiceProtocol(
    Auditable,
    Protocol[Spec_contra, Result_cov],
):
    """Protocol for user's service follows the specification."""

    def execute(self, user: Person, spec: Spec_contra) -> Result_cov:
        """Execute."""


PresentationServiceProtocol = UserSpecServiceProtocol[
    ExerciseConfigProtocol,
    PresentationCaseProtocol,
]

TestServiceProtocol = UserSpecServiceProtocol[
    ExerciseConfigProtocol,
    TestCaseProtocol,
]
