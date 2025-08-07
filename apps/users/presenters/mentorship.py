"""Defines mentorship relations presenter."""

from django.db.models import F, QuerySet

from apps.users.models import CustomUser
from apps.users.models.mentorship import Mentorship, MentorshipRequest


class MentorshipPresenter:
    """Mentorship relations presenter."""

    @staticmethod
    def _get_requests_to_mentors(
        user: CustomUser,
    ) -> QuerySet:  # type: ignore[type-arg]
        """Get mentorship requests sent by user to potential mentors."""
        return (
            MentorshipRequest.objects.filter(from_user=user)
            .annotate(
                request_pk=F('pk'),
                mentor_name=F('to_user__username'),
            )
            .values('request_pk', 'mentor_name')
        )

    @staticmethod
    def _get_requests_from_students(
        user: CustomUser,
    ) -> QuerySet:  # type: ignore[type-arg]
        """Get mentorship requests received by user from students."""
        return (
            MentorshipRequest.objects.filter(to_user=user)
            .annotate(
                request_pk=F('pk'),
                student_name=F('from_user__username'),
            )
            .values('request_pk', 'student_name')
        )

    @staticmethod
    def _get_current_students(
        user: CustomUser,
    ) -> QuerySet:  # type: ignore[type-arg]
        """Get current students of the user (as a mentor)."""
        return (
            Mentorship.objects.filter(mentor=user)
            .annotate(
                student_pk=F('student__pk'),
                student_name=F('student__username'),
            )
            .values('id', 'student_pk', 'student_name')
        )

    @staticmethod
    def _get_current_mentors(
        user: CustomUser,
    ) -> QuerySet:  # type: ignore[type-arg]
        """Get current mentors of the user (as a student)."""
        return (
            Mentorship.objects.filter(student=user)
            .annotate(mentor_name=F('mentor__username'))
            .values('id', 'mentor_name')
        )

    def get_mentorship_relations(
        self,
        user: CustomUser,
    ) -> dict[str, QuerySet]:  # type: ignore[type-arg]
        """Get all mentorship relations for a given user.

        Returns:
            Dictionary containing:
            - to_mentor: Requests sent to potential mentors
            - from_student: Requests received from students
            - students: Current students (when user is mentor)
            - mentors: Current mentors (when user is student)

        """
        return {
            'to_mentor': self._get_requests_to_mentors(user),
            'from_student': self._get_requests_from_students(user),
            'students': self._get_current_students(user),
            'mentors': self._get_current_mentors(user),
        }
