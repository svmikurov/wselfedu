"""Defines user profile view."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView


class ProfileView(UserPassesTestMixin, DetailView):  # type: ignore[type-arg]
    """User profile view."""

    model = get_user_model()
    template_name = 'users/profile.html'

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        return bool(self.request.user == self.get_object())
