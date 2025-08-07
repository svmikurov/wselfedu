"""Defines mentorship views."""

from typing import Any

from django.views.generic import CreateView, TemplateView

from apps.core.generic.views import HtmxDeleteView

from ..forms import SendMentorshipRequest
from ..models import Mentorship, MentorshipRequest


class MentorshipView(TemplateView):
    """Mentorship view."""

    template_name = 'users/mentorship.html'

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add context data."""
        user = self.request.user
        context = super().get_context_data(**kwargs)

        context['mentor_mentorships'] = Mentorship.objects.filter(  # type: ignore[misc]
            mentor=user,
        )
        context['student_mentorships'] = Mentorship.objects.filter(  # type: ignore[misc]
            student=user,
        )
        context['request_from_students'] = MentorshipRequest.objects.filter(  # type: ignore[misc]
            to_user=user,
        )
        context['request_to_mentors'] = MentorshipRequest.objects.filter(  # type: ignore[misc]
            from_user=user,
        )
        context['form'] = SendMentorshipRequest()

        return context


class SendMentorRequestView(CreateView):  # type: ignore[type-arg]
    """Send request of mentorship to mentor."""

    model = MentorshipRequest


class DeleteStudentView(HtmxDeleteView):
    """Delete the student from mentorship."""

    model = Mentorship

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        return bool(self.request.user == self.get_object().mentor)


class DeleteMentorView(HtmxDeleteView):
    """Delete the mentor from mentorship."""

    model = Mentorship

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        return bool(self.request.user == self.get_object().student)


class DeleteStudentRequestView(HtmxDeleteView):
    """Delete the request from student on mentorship."""

    model = MentorshipRequest

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        return bool(self.request.user == self.get_object().to_user)


class DeleteMentorRequestView(HtmxDeleteView):
    """Delete the request to mentor on mentorship."""

    model = MentorshipRequest

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        return bool(self.request.user == self.get_object().from_user)
