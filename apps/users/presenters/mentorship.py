"""Defines mentorship relations presenter."""

from django.db.models import QuerySet
from typing_extensions import override

from apps.users.models import Person
from apps.users.models.mentorship import Mentorship, MentorshipRequest
from apps.users.presenters.iabc import MentorshipPresenterABC


class MentorshipPresenter(MentorshipPresenterABC):
    """Mentorship relations presenter."""

    @staticmethod
    @override
    def get_requests_to_mentors(
        student: Person,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests sent by user to potential mentors."""
        return MentorshipRequest.objects.filter(from_user=student)

    @staticmethod
    @override
    def get_requests_from_students(
        mentor: Person,
    ) -> QuerySet[MentorshipRequest]:
        """Get mentorship requests received by user from students."""
        return MentorshipRequest.objects.filter(to_user=mentor)

    @staticmethod
    @override
    def get_students(mentor: Person) -> QuerySet[Mentorship]:
        """Get students for a specific mentor."""
        return Mentorship.objects.filter(mentor=mentor)

    @staticmethod
    @override
    def get_mentors(student: Person) -> QuerySet[Mentorship]:
        """Get mentors for a specific student."""
        return Mentorship.objects.filter(student=student)

    @classmethod
    @override
    def get_mentorship_relations(
        cls,
        user: Person,
    ) -> dict[str, QuerySet[MentorshipRequest | Mentorship]]:
        """Get all mentorship relations for a given user."""
        return {
            'mentor_mentorships': cls.get_students(user),
            'request_from_students': cls.get_requests_from_students(user),
            'student_mentorships': cls.get_mentors(user),
            'request_to_mentors': cls.get_requests_to_mentors(user),
        }
