"""Mentorship mixins."""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpRequest

from users.models import Mentorship


class CheckMentorshipMixin(UserPassesTestMixin):
    """Mixin to check if a mentoring relationship exists."""

    request: HttpRequest
    template_name = 'users/mentorship/assign_to_student.html'

    def test_func(self) -> bool:
        """Test if there is a mentoring relationship."""
        return Mentorship.objects.filter(
            mentor=self.request.user.id,
            student=self.request.resolver_match.kwargs.get('student_id'),
        ).exists()
