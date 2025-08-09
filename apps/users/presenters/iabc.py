"""Defines protocols and ABC for Users app presenters interface."""

from abc import ABC, abstractmethod
from typing import Protocol

from django.db.models.query import QuerySet
from typing_extensions import override

from ..models import (
    AssignedExercise,
    CustomUser,
    Mentorship,
    MentorshipRequest,
)


class IMentorshipPresenter(Protocol):
    """Protocol for mentorship relations presenter."""

    @staticmethod
    def get_requests_to_mentors(
        student: CustomUser,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests sent by user to potential mentors."""

    @staticmethod
    def get_requests_from_students(
        mentor: CustomUser,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests received by user from students."""

    @staticmethod
    def get_students(mentor: CustomUser) -> QuerySet[Mentorship]:
        """Get students for a specific mentor."""

    @staticmethod
    def get_mentors(student: CustomUser) -> QuerySet[Mentorship]:
        """Get mentors for a specific student."""

    @classmethod
    def get_mentorship_relations(
        cls,
        user: CustomUser,
    ) -> dict[str, QuerySet[MentorshipRequest | Mentorship]]:
        """Get all mentorship relations for a given user."""


class MentorshipPresenterABC(IMentorshipPresenter, ABC):
    """Protocol for mentorship relations presenter."""

    @staticmethod
    @abstractmethod
    @override
    def get_requests_to_mentors(
        student: CustomUser,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests sent by user to potential mentors."""

    @staticmethod
    @abstractmethod
    @override
    def get_requests_from_students(
        mentor: CustomUser,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests received by user from students."""

    @staticmethod
    @abstractmethod
    @override
    def get_students(mentor: CustomUser) -> QuerySet[Mentorship]:
        """Get students for a specific mentor."""

    @staticmethod
    @abstractmethod
    @override
    def get_mentors(student: CustomUser) -> QuerySet[Mentorship]:
        """Get mentors for a specific student."""

    @classmethod
    @abstractmethod
    @override
    def get_mentorship_relations(
        cls,
        user: CustomUser,
    ) -> dict[str, QuerySet[MentorshipRequest | Mentorship]]:
        """Get all mentorship relations for a given user."""


class IStudentExercisesPresenter(Protocol):
    """Protocol for student exercise presenter interface."""

    @staticmethod
    def get_assigned(
        mentorship: Mentorship | None = None,
    ) -> QuerySet[AssignedExercise]:
        """Get assigned exercises to student by mentor."""


class StudentExercisesPresenterABC(IStudentExercisesPresenter, ABC):
    """Abstract base class for student exercise presenter."""

    @staticmethod
    @abstractmethod
    @override
    def get_assigned(
        mentorship: Mentorship | None = None,
    ) -> QuerySet[AssignedExercise]:
        """Get assigned exercises to student by mentor."""
