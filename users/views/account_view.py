from django.db.models import F
from django.views.generic import DetailView

from contrib.mixins_views import CheckObjectOwnershipMixin
from users.models import UserModel, Mentorship, MentorshipRequest


class UserDetailView(CheckObjectOwnershipMixin, DetailView):
    """User detail view."""

    template_name = 'users/detail.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        """Add data to context."""
        mentorship_request_mentors = MentorshipRequest.objects.filter(
            from_user=self.request.user
        ).annotate(
            request_pk=F('pk'),
            mentor_name=F('to_user__username'),
        ).values('request_pk', 'mentor_name')

        mentorship_request_students = MentorshipRequest.objects.filter(
            to_user=self.request.user
        ).annotate(
            request_pk=F('pk'),
            student_name=F('from_user__username'),
        ).values('request_pk', 'student_name')

        mentorship_students = Mentorship.objects.filter(
            mentor=self.request.user,
        ).annotate(
            student_name=F('student__username'),
        ).values('id', 'student_name')

        mentorship_mentors = Mentorship.objects.filter(
            student=self.request.user,
        ).annotate(
            mentor_name=F('mentor__username')
        ).values('id', 'mentor_name')

        context = super().get_context_data()
        context['mentorship_request_mentors'] = mentorship_request_mentors
        context['mentorship_request_students'] = mentorship_request_students
        context['mentorship_students'] = mentorship_students
        context['mentorship_mentors'] = mentorship_mentors
        return context
