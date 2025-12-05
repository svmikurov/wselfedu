"""Defines protocols and ABC for Users app presenters interface."""

from abc import ABC, abstractmethod
from typing import Protocol

from django.db.models.query import QuerySet
from typing_extensions import override

from apps.study.models import ExerciseAssigned

from ..models import (
    Mentorship,
    MentorshipRequest,
    Person,
)


class IMentorshipPresenter(Protocol):
    """Protocol for mentorship relations presenter."""

    @staticmethod
    def get_requests_to_mentors(
        student: Person,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests sent by user to potential mentors."""

    @staticmethod
    def get_requests_from_students(
        mentor: Person,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests received by user from students."""

    @staticmethod
    def get_students(mentor: Person) -> QuerySet[Mentorship]:
        """Get students for a specific mentor."""

    @staticmethod
    def get_mentors(student: Person) -> QuerySet[Mentorship]:
        """Get mentors for a specific student."""

    @classmethod
    def get_mentorship_relations(
        cls,
        user: Person,
    ) -> dict[str, QuerySet[MentorshipRequest | Mentorship]]:
        """Get all mentorship relations for a given user."""


class MentorshipPresenterABC(IMentorshipPresenter, ABC):
    """Protocol for mentorship relations presenter."""

    @staticmethod
    @abstractmethod
    @override
    def get_requests_to_mentors(
        student: Person,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests sent by user to potential mentors."""

    @staticmethod
    @abstractmethod
    @override
    def get_requests_from_students(
        mentor: Person,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests received by user from students."""

    @staticmethod
    @abstractmethod
    @override
    def get_students(mentor: Person) -> QuerySet[Mentorship]:
        """Get students for a specific mentor."""

    @staticmethod
    @abstractmethod
    @override
    def get_mentors(student: Person) -> QuerySet[Mentorship]:
        """Get mentors for a specific student."""

    @classmethod
    @abstractmethod
    @override
    def get_mentorship_relations(
        cls,
        user: Person,
    ) -> dict[str, QuerySet[MentorshipRequest | Mentorship]]:
        """Get all mentorship relations for a given user."""


class IStudentExercisesPresenter(Protocol):
    """Protocol for student exercise presenter interface.

    Presents to render the exercises assigned by the mentor.
    """

    @classmethod
    def get_assigned_by_mentor(
        cls,
        mentorship: Mentorship,
    ) -> QuerySet[ExerciseAssigned]:
        """Get assigned exercises to student by mentor."""

    @classmethod
    def get_assigned_all(
        cls,
        student: Person,
    ) -> QuerySet[ExerciseAssigned]:
        """Get assigned exercises to student by all his mentors."""

    @classmethod
    def get_exercise_meta(
        cls,
        assignation_id: int,
        student: Person,
    ) -> ExerciseAssigned:
        """Get assigned exercise meta data."""


class StudentExercisesPresenterABC(IStudentExercisesPresenter, ABC):
    """Abstract base class for student exercise presenter."""

    @classmethod
    @abstractmethod
    @override
    def get_assigned_by_mentor(
        cls,
        mentorship: Mentorship,
    ) -> QuerySet[ExerciseAssigned]:
        """Get assigned exercises to student by mentor."""

    @classmethod
    @abstractmethod
    @override
    def get_assigned_all(
        cls,
        student: Person,
    ) -> QuerySet[ExerciseAssigned]:
        """Get assigned exercises to student by all his mentors."""

    @classmethod
    @abstractmethod
    @override
    def get_exercise_meta(
        cls,
        assignation_id: int,
        student: Person,
    ) -> ExerciseAssigned:
        """Get assigned exercise meta data."""
