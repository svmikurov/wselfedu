"""Defines protocols and ABC for Users app services interface."""

from abc import ABC, abstractmethod
from typing import Protocol

from typing_extensions import override

from apps.users.models import MentorshipRequest, Person


class IMentorshipService(Protocol):
    """Protocol for mentorship service interface."""

    @staticmethod
    def create_mentorship_request(
        student: Person,
        mentor_username: str,
    ) -> MentorshipRequest:
        """Create mentorship request."""

    @staticmethod
    def accept_mentorship_request(request_id: int, mentor: Person) -> None:
        """Accept by mentor the user request to mentorship."""


class MentorshipServiceABC(IMentorshipService, ABC):
    """Abstract base class for mentorship service."""

    @staticmethod
    @abstractmethod
    @override
    def create_mentorship_request(
        student: Person,
        mentor_username: str,
    ) -> MentorshipRequest:
        """Create mentorship request."""

    @staticmethod
    @abstractmethod
    @override
    def accept_mentorship_request(request_id: int, mentor: Person) -> None:
        """Accept by mentor the user request to mentorship."""
