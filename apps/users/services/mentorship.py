"""Defines mentorship service."""

from django.shortcuts import get_object_or_404
from typing_extensions import override

from apps.users.exception import MentorshipError
from apps.users.models import Mentorship, MentorshipRequest, Person
from apps.users.services.iabc import MentorshipServiceABC


class MentorshipService(MentorshipServiceABC):
    """Mentorship service."""

    @staticmethod
    @override
    def create_mentorship_request(
        student: Person,
        mentor_username: str,
    ) -> MentorshipRequest:
        """Create mentorship request."""
        mentor = Person.objects.filter(username=mentor_username).first()

        if not mentor:
            raise MentorshipError(
                f'Requested "{mentor_username}" not found',
                html_message=f'Ментор "{mentor_username}" не найден.',
            )

        if student == mentor:
            raise MentorshipError(
                'Student try send request for mentorship itself',
                html_message='Нельзя отправит запрос на наставничество себе',
            )

        if Mentorship.objects.filter(mentor=mentor, student=student).exists():
            raise MentorshipError(
                'Mentoring already exists',
                html_message=f'"{mentor_username}" уже ваш наставник',
            )

        mentorship_request, created = MentorshipRequest.objects.get_or_create(
            from_user=student, to_user=mentor
        )

        if not created:
            raise MentorshipError(
                f'Request to {mentor} already send',
                html_message=f'Запрос "{mentor_username}" уже направлен ранее',
            )

        return mentorship_request

    @staticmethod
    @override
    def accept_mentorship_request(request_id: int, mentor: Person) -> None:
        """Accept by mentor the user request to mentorship."""
        mentorship_request = get_object_or_404(
            MentorshipRequest,
            pk=request_id,
            to_user=mentor,
        )
        Mentorship.objects.create(
            mentor=mentor,
            student=mentorship_request.from_user,
        )
        mentorship_request.delete()
