"""Defines user profile view."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView

from ..models import CustomUser
from ..presenters.mentorship import MentorshipPresenter


class ProfileView(UserPassesTestMixin, DetailView):  # type: ignore[type-arg]
    """User profile view."""

    model = get_user_model()
    template_name = 'users/profile.html'
    mentorship_presenter_class = MentorshipPresenter

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        return bool(self.request.user == self.get_object())

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        """Add data to context data."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if isinstance(user, CustomUser):
            presenter = self.mentorship_presenter_class()
            context.update(presenter.get_mentorship_relations(user))
        return context
