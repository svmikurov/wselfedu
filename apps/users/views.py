"""Defines Users app views."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import SignUpForm


class SignUpView(CreateView):  # type: ignore[type-arg]
    """User sign up view."""

    model = get_user_model()
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(UserPassesTestMixin, DetailView):  # type: ignore[type-arg]
    """User profile view."""

    model = get_user_model()
    template_name = 'account.html'

    def test_func(self) -> bool:
        """Check if the user is the owner of the object."""
        return bool(self.request.user == self.get_object())
