"""Protocols for exercise domain interface."""

from typing import Protocol, TypeVar

from ports.interfaces.protocols.domain.exercise import CandidatesT
from utils.audit.protocol import Auditable

ExerciseConfig_contra = TypeVar('ExerciseConfig_contra', contravariant=True)
Domain_contra = TypeVar('Domain_contra', contravariant=True)
Option_co = TypeVar('Option_co', covariant=True)

Answer_contra = TypeVar('Answer_contra', contravariant=True)
Case_contra = TypeVar('Case_contra', contravariant=True)
Result_co = TypeVar('Result_co', covariant=True)


class CreateTaskDomainProtocol(
    Protocol[
        ExerciseConfig_contra,
        Option_co,
    ],
):
    """Protocol for create exercise task domain interface."""

    def execute(
        self,
        candidates: CandidatesT,
        conf: ExerciseConfig_contra,
    ) -> Option_co:
        """Create exercise case."""


class CheckTaskDomainProtocol(
    Auditable,
    Protocol[
        Answer_contra,
        Case_contra,
        Result_co,
    ],
):
    """Protocol for create exercise task domain interface."""

    def execute(
        self,
        answer: Answer_contra,
        case: Case_contra,
    ) -> Result_co:
        """Create exercise case."""


class ExpalinAnswerDomainProtocol(
    Auditable,
    Protocol[
        Answer_contra,
        Domain_contra,
        Result_co,
    ],
):
    """Protocol for explain answer domain interface."""

    def execute(
        self,
        answer: Answer_contra,
        domain: Domain_contra,
    ) -> Result_co:
        """Create exercise case."""
