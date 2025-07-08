"""Defines account views."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView


class AccountView(UserPassesTestMixin, DetailView):  # type: ignore[type-arg]
    """Account view."""

    model = get_user_model()
    template_name = 'users/account.html'

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        return bool(self.request.user == self.get_object())
